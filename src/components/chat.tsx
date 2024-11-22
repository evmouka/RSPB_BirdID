import React, { useState } from "react";
import RspbIcon from "./rspb-icon"; // Replace with your RSPB icon import
import UserIcon from "./user-icon"; // Replace with your User icon import
import InfoIcon from "./info-icon"; // Replace with your Info icon import

interface Message {
  sender: "chatbot" | "user";
  content: string;
}

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
    //   const response = await fetch("../data/dummy/anwers.json");
    //     console.log(response);
    //   if (!response.ok) throw new Error("Failed to fetch response");

    //   let data = await response.json();

      const data = [{
        "isConfused": false,
        "categoryPrompt": "beak shape",
        "identifications": null,
        "categories": {
            "Plumage colour(s)": "black, gray",
            "Tail shape 1": "fan",
            "Size": "small"
        }}]

    
        console.log(data);
      setMessages((prev) => [
        ...prev.slice(0, -1),
        { sender: "chatbot", content: data[0].categoryPrompt },
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev.slice(0, -1),
        { sender: "chatbot", content: "Oops! Something went wrong. Please try again." },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen w-full max-w-3xl mx-auto bg-gray-100">
      {/* Chat Messages Section */}
      <div className="flex-1 p-4 overflow-y-auto">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`flex items-start mb-4 ${
              msg.sender === "user" ? "justify-end" : "justify-start"
            }`}
          >
            <div className={`flex items-center ${msg.sender === "user" ? "flex-row-reverse" : ""}`}>
              <div className="shrink-0">
                {msg.sender === "user" ? <UserIcon /> : <RspbIcon />}
              </div>
              <div
                className={`px-4 py-2 rounded-xl shadow-md max-w-xs ${
                  msg.sender === "user"
                    ? "bg-teal-900 text-white rounded-tr"
                    : "bg-white text-gray-700 rounded-tl"
                }`}
              >
                <h2 className="opacity-75 text-sm uppercase">
                  {msg.sender === "user" ? "You" : "Chat RSPB"}
                </h2>
                <p>{msg.content}</p>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Footer Section */}
      <div className="p-4 bg-white border-t shadow-md">
        <div className="flex items-center">
          <InfoIcon className="w-6 h-6 text-blue-500 mr-2" />
          <p className="text-sm text-gray-600 flex-grow">
            For example: <em>Small, fluffy, blue bird in my garden</em>
          </p>
        </div>
        <div className="flex items-center mt-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your message..."
            className="flex-1 px-4 py-2 border rounded-full focus:outline-none focus:ring focus:ring-blue-300"
            disabled={isLoading}
          />
          <button
            onClick={handleSend}
            className="ml-4 w-10 h-10 flex items-center justify-center bg-blue-500 text-white rounded-full shadow-md hover:bg-blue-600"
            disabled={isLoading}
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="w-6 h-6"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M14.7 6.3a1 1 0 011.4 0l4.6 4.6a1 1 0 010 1.4l-4.6 4.6a1 1 0 01-1.4-1.4L18.3 12H3a1 1 0 010-2h15.3l-3.6-3.6a1 1 0 010-1.4z"
              />
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
};

export default Chat;


