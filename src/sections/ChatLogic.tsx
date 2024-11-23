import { useState, useEffect } from "react";
import InfoIcon from "../components/info-icon.tsx";
import ChatBubble from "../components/chat-bubble.tsx";
import categoryPrompts from "../categoryPrompts.json";

interface CategoryPrompts {
  [key: string]: string;
}

interface Message {
  sender: "chatbot" | "user";
  content: string;
}

const prompts: CategoryPrompts = categoryPrompts;

interface ResponseData {
  isConfused: boolean;
  category_prompt: string;
  identifications: any;
  categories: Record<string, string>;
}

const Chat: React.FC = () => {
  // Initialize chat messages to the default greeting (doesn't load the full history on reload)
  const [messages, setMessages] = useState<Message[]>([
    {
      sender: "chatbot",
      content: "Hi! Describe the bird you spotted, and I'll try to identify it.",
    },
  ]);

  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [prompt, setPrompt] = useState("");
  const [categories, setCategories] = useState({});
  const [conversationEnded, setConversationEnded] = useState(false);
  const [hasSentFirstMessage, setHasSentFirstMessage] = useState(false);

  // Save chat history to localStorage when the conversation ends
  useEffect(() => {
    if (conversationEnded || hasSentFirstMessage) {
      localStorage.setItem("chatHistory", JSON.stringify(messages));
    }
  }, [messages, conversationEnded, hasSentFirstMessage]);

  // Handle sending messages
  const handleSend = async () => {
    if (input.trim() === "") return;

    // Mark that the user has sent their first message
    if (!hasSentFirstMessage) {
      setHasSentFirstMessage(true);
    }

    const userMessage: Message = { sender: "user", content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");

    setIsLoading(true);
    const loadingMessage: Message = { sender: "chatbot", content: "..." };
    setMessages((prev) => [...prev, loadingMessage]);

    try {
      const res = await fetch("http://localhost:5000/birds", {
        method: "POST",
        headers: {
          "Content-Type": "Application/json",
        },
        body: JSON.stringify({
          message: userMessage.content,
          categoryPrompt: prompt,
          categories: categories,
        }),
      });

      if (!res.ok) throw new Error("Failed to fetch response");

      const response: ResponseData = await res.json();
      console.log(response);

      // Handle `isConfused`
      if (response.isConfused) {
        setMessages((prev) => [
          ...prev.slice(0, -1),
          {
            sender: "chatbot",
            content: "I'm not sure I understand. Could you provide more details?",
          },
        ]);
      } else if (response.identifications && response.identifications.length > 0) {
        // Bird identification successful
        setMessages((prev) => [
          ...prev.slice(0, -1),
          {
            sender: "chatbot",
            content: `I think this is a ${response.identifications[0].Name} (${response.identifications[0].LatinName}).`,
          },
        ]);
        setConversationEnded(true); // Mark conversation as ended
      } else {
        // Handle category prompts
        let promptKey = response.category_prompt;
        if (promptKey === "beak shape") {
          promptKey = "Beak Shape 1";
        }

        setMessages((prev) => [
          ...prev.slice(0, -1),
          { sender: "chatbot", content: prompts[promptKey] },
        ]);

        setPrompt(promptKey);
        setCategories(response.categories);
      }
    } catch (error) {
      console.error(error);
      setMessages((prev) => [
        ...prev.slice(0, -1),
        {
          sender: "chatbot",
          content: "Oops! Something went wrong. Please try again.",
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDownloadChatHistory = () => {
    const chatData = messages
      .map(
        (msg) =>
          `${msg.sender === "user" ? "You" : "Chatbot"}: ${msg.content}`
      )
      .join("\n");
    const blob = new Blob([chatData], { type: "text/plain" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "chat-history.txt";
    link.click();
  };

  return (
    <div className="flex flex-col h-screen w-full">
      <main className="flex justify-center basis-full p-6 bg-gray-200">
        <div className="flex flex-col gap-4 w-full max-w-screen-sm">
          {messages.map((msg, index) => (
            <div key={index}>
              <ChatBubble sender={msg.sender} content={msg.content} />
            </div>
          ))}

          {/* Display chat history when the conversation ends */}
          {conversationEnded && (
            <div className="mt-4 p-4 bg-gray-100 rounded shadow">
              <h3 className="font-bold">Chat History</h3>
              <ul className="list-disc pl-4">
                {messages.map((msg, index) => (
                  <li key={index} className="my-1">
                    <strong>{msg.sender === "user" ? "You" : "Chatbot"}:</strong>{" "}
                    {msg.content}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </main>
      <footer className="flex flex-col items-center justify-center p-6 border-t-2 shadow-sm">
        <div className="w-full max-w-screen-sm">
          {!conversationEnded && !hasSentFirstMessage && (
            <>
              <h3 className="font-semibold">For example</h3>
              <p className="px-2 py-3 rounded-sm bg-gray-100 text-gray-500 italic">
                Small, fluffy, blue bird on my garden feeder
              </p>
              <div className="flex gap-2 my-3">
                <InfoIcon />
                <div>
                  <p>What to include in my description</p>
                  <hr className="w-24 -mt-0.5 border border-sky-500" />
                </div>
              </div>
            </>
          )}
          <div className="flex items-center mt-2">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type your message..."
              disabled={isLoading || conversationEnded}
              className="flex-1 px-6 py-3 border rounded-full border-gray-400 placeholder:text-gray-500"
            />
            <button
              onClick={handleSend}
              disabled={isLoading || conversationEnded}
              className="ml-4 w-10 h-10 flex items-center justify-center rounded-full"
            >
              <svg className="w-6 h-6" viewBox="0 0 28 28">
                <path
                  d="M5.86667 25.9C5.42222 26.0778 5 26.0389 4.6 25.7833C4.2 25.5278 4 25.1556 4 24.6667V18.6667L14.6667 16L4 13.3333V7.33334C4 6.84445 4.2 6.47222 4.6 6.21667C5 5.96111 5.42222 5.92222 5.86667 6.1L26.4 14.7667C26.9556 15.0111 27.2333 15.4222 27.2333 16C27.2333 16.5778 26.9556 16.9889 26.4 17.2333L5.86667 25.9Z"
                  fill="#0099FB"
                />
              </svg>
            </button>
          </div>
        </div>
        {messages.length > 0 && (
          <button
            onClick={handleDownloadChatHistory}
            className="mt-4 bg-blue-500 text-white px-4 py-2 rounded-full"
          >
            Download Chat History
          </button>
        )}
      </footer>
    </div>
  );
};

export default Chat;
