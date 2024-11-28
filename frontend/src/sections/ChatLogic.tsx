import { useState, useEffect } from "react";
import InfoIcon from "../components/info-icon.tsx";
import ChatBubble from "../components/chat-bubble.tsx";
import categoryPrompts from "../categoryPrompts.json";
import BirdIdentity from "../components/birdIdentity.tsx";
import BirdSelection from "../components/BirdSelection.tsx";
import GameMode from "../components/GameMode.tsx";

interface CategoryPrompts {
  [key: string]: string;
}

interface Message {
  sender: "chatbot" | "user";
  content: string;
}

interface Identification {
  name: string;
  picture: string;
  summary: string;
  user_data: any;
}

type Identifications = Identification[];

const Chat: React.FC = () => {
  const prompts: CategoryPrompts = categoryPrompts;
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
  const [imageSrc, setImageSrc] = useState("");
  const [birdName, SetBirdName] = useState("");
  const [hasSentFirstMessage, setHasSentFirstMessage] = useState(false);
  const [userData, setUserData] = useState<any>("");
  const [birdResults, setBirdResults] = useState<any[]>([]);

  useEffect(() => {
    if (birdResults.length > 1) {
      setMessages((prev) => [
        ...prev,
        {
          sender: "chatbot",
          content:
            "Based on your description, we believe you might have spotted one of these birds. Please select the one you think it is.",
        },
      ]);
    } else if (birdResults.length === 1) {
      setMessages((prev) => [
        ...prev,
        {
          sender: "chatbot",
          content:
            "Based on your description, it seems you saw a " +
            birdResults[0].name +
            ". " +
            birdResults[0].summary,
        },
      ]);
    }
  }, [birdResults]);

  useEffect(() => {
    if (hasSentFirstMessage) {
      localStorage.setItem("chatHistory", JSON.stringify(messages));
    }
  }, [messages, hasSentFirstMessage]);

  const fetchBirdData = async (userMessage: Message, updatedCategories = categories) => {
    setIsLoading(true);
    const loadingMessage: Message = { sender: "chatbot", content: "..." };
    setMessages((prev) => [...prev, loadingMessage]);

    try {
      const response = await fetch("http://localhost:5000/birds", {
        method: "POST",
        headers: {
          "Content-Type": "Application/json",
        },
        body: JSON.stringify({
          message: userMessage.content,
          categoryPrompt: prompt,
          categories: updatedCategories,
          user_data: userData,
          birdId: -1,
        }),
      });

      if (!response.ok) throw new Error("Failed to fetch response");
      const data = (await response.json()).data;
      const newPrompt = data.category_prompt;
      const birdResult: Identifications = data.identifications;

      if (data.isConfused) {
        setMessages((prev) => [
          ...prev.slice(0, -1),
          {
            sender: "chatbot",
            content: "I'm not sure I understand. Could you provide more details?",
          },
        ]);
      } else {
        const processedSummary = processSummary(data.categories);
        setMessages((prev) => [
          ...prev.slice(0, -1),
          { sender: "chatbot", content: processedSummary },
        ]);

        if (birdResult != null) {
          if (birdResult.length > 0) {
            setBirdResults(birdResult);
            setImageSrc(birdResult[0].picture);
            SetBirdName(birdResult[0].name);
          }
        }

        setTimeout(() => {
          if (newPrompt != null) {
            setMessages((prev) => [
              ...prev,
              { sender: "chatbot", content: prompts[newPrompt] },
            ]);
          }
        }, 500);

        setPrompt(newPrompt);
        setCategories(data.categories);
        setUserData(data.user_data);
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

  const handleSend = async () => {
    if (input.trim() === "") return;

    if (!hasSentFirstMessage) {
      setHasSentFirstMessage(true);
    }

    const userMessage: Message = { sender: "user", content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");

    await fetchBirdData(userMessage);
  };

  function processSummary(userInput) {
    const templates = {
        plumage_colour: "The bird has a plumage that is described as {}.",
        beak_colour: "Its beak is coloured {}.",
        feet_colour: "The feet of the bird appear {}.",
        leg_colour: "Its legs are {}.",
        beak_shape_1: "The beak is shaped {}.",
        tail_shape_1: "It has a tail that is {}.",
        pattern_markings: "There are visible markings or patterns described as {}.",
        size: "The bird is {} in size.",
        habitat: "It is commonly found in habitats described as {}."
    };
    const updatedCategories = JSON.parse(JSON.stringify(userInput));

    const keywords = new Set();
    const summaryParts = [];

    for (const [category, adjectives] of Object.entries(updatedCategories)) {
        if (templates[category] && adjectives) {
            const formattedAdjectives = Array.isArray(adjectives)
                ? adjectives.join(", ")
                : adjectives;
            summaryParts.push(templates[category].replace("{}", formattedAdjectives));

            if (Array.isArray(adjectives)) {
                adjectives.forEach(adj => keywords.add(adj));
            } else {
                keywords.add(adjectives);
            }
        }
    }

    const summary = summaryParts.join(" ");

    const regex = new RegExp(`\\b(${Array.from(keywords).join("|")})\\b`, "gi");
    const parts = summary.split(regex);

    return parts.map((part, index) => {
        const lowercasePart = part.toLowerCase();
        if (keywords.has(lowercasePart)) {
            return (
                <span key={index} className="highlight-bubble">
                    {part}
                    <button
                        className="close"
                        onClick={(e) => {
                            e.stopPropagation();
                            const newCategories = {...updatedCategories};
                            for (const [category, value] of Object.entries(newCategories)) {
                                if (Array.isArray(value)) {
                                    const filteredValue = value.filter(
                                        v => v.toLowerCase() !== lowercasePart
                                    );
                                    if (filteredValue.length > 0) {
                                        newCategories[category] = filteredValue;
                                    } else {
                                        delete newCategories[category];
                                    }
                                } else if (typeof value === 'string') {
                                    if (value.toLowerCase() === lowercasePart) {
                                        delete newCategories[category];
                                    }
                                }
                            }
                                    setCategories((prev) => {
                                      fetchBirdData({ sender: "user", content: "" }, newCategories);
                                      return newCategories;
                                    });
                        }}
                    >
                    </button>
                </span>
            );
        }
        return part;
    });
}

  return (
    <div className="flex flex-col h-screen w-full">
      <GameMode />
      <main className="flex justify-center basis-full p-6 bg-gray-200">
        <div className="flex flex-col gap-4 w-full max-w-screen-sm">
          {messages.map((msg, index) => (
            <div key={index}>
              <ChatBubble sender={msg.sender} content={msg.content} />
            </div>
          ))}
          {}
          {birdResults.length > 1 ? (
            <>
              {}
              <BirdSelection
                birdResults={birdResults}
                setBirdResults={setBirdResults}
                setImageSrc={setImageSrc}
                SetBirdName={SetBirdName}
                // SetBirdSummary={setBirdSummary}
              />
            </>
          ) : birdResults.length === 1 ? (
            <BirdIdentity
              birdData={birdResults[0]}
              imageSrc={birdResults[0].picture}
              birdName={birdResults[0].name}
              // birdSummary={birdResults[0].summary}
              imageSize="100%"
            />
          ) : null}
        </div>
      </main>

      <footer className="flex justify-center p-6 border-t-2 shadow-sm sticky bottom-0 bg-white">
        <div className="w-full max-w-screen-sm">
          {!hasSentFirstMessage && (
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
              onKeyDown={(e) => {
                if (e.key === "Enter") handleSend();
              }}
              placeholder="Type your message..."
              disabled={isLoading}
              className="flex-1 px-6 py-3 border rounded-full border-gray-400 placeholder:text-gray-500"
            />
            <button
              onClick={handleSend}
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