import { useState } from "react";
import { Message } from "../types/Message.ts";
import InfoIcon from "../components/info-icon.tsx"
import ChatBubble from "../components/chat-bubble.tsx"

const Chat: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      sender: "chatbot",
      content: "Hi! Describe the bird you spotted, and I'll try to identify it.",
    },
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleSend = async () => {
    if (input.trim() === "") return;

    const userMessage: Message = { sender: "user", content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");

    setIsLoading(true);
    const loadingMessage: Message = { sender: "chatbot", content: "..." };
    setMessages((prev) => [...prev, loadingMessage]);

    try {
//fetch request will be here
      const data = {
        isConfused: false,
        categoryPrompt: "beak shape",
        identifications: null,
        categories: {
          "Plumage colour(s)": "black, gray",
          "Tail shape 1": "fan",
          Size: "small",
        },
      };

      if (data && data.categoryPrompt) {
        console.log(data.categoryPrompt);
        setMessages((prev) => [
          ...prev.slice(0, -1),
          { sender: "chatbot", content: data.categoryPrompt },
        ]);
      }
    } catch (error) {
      console.error(error);
      setMessages((prev) => [
        ...prev.slice(0, -1),
        { sender: "chatbot", content: "Oops! Something went wrong. Please try again." },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return(
    <div className="flex flex-col h-screen w-full ">
        <main className="flex justify-center basis-full p-6 bg-gray-200">
        <div className="flex flex-col gap-4 w-full max-w-screen-sm">
            {messages.map((msg, index) => (
            <div key={index}>
                <ChatBubble
                sender={msg.sender}
                content={msg.content}
                />
            </div>
            ))}
        </div>
        </main>
        <footer className="flex justify-center p-6 border-t-2 shadow-sm">
            <div className="w-full max-w-screen-sm">
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
                <div className="flex items-center mt-2">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="Type your message..."
                        disabled={isLoading}
                        className="flex-1 px-6 py-3 border rounded-full border-gray-400 placeholder:text-gray-500"
                    />
                    <button
                        onClick={handleSend} //working :D
                        disabled={isLoading}
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
        </footer>
    </div>
  );
};

export default Chat;
