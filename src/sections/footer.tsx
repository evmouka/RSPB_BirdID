import React, { useState } from "react";

interface FooterProps {
  onSend: (message: string) => void; // Callback to send a message
}

const Footer: React.FC<FooterProps> = ({ onSend }) => {
  const [input, setInput] = useState("");

  const handleSend = () => {
    if (input.trim() === "") return;
    onSend(input); // Call the parent send function
    setInput(""); // Clear input after sending
  };

  return (
    <div className="flex items-center justify-between p-4 bg-white border-t shadow-md">
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Type your message..."
        className="flex-1 px-4 py-2 border rounded-full focus:outline-none focus:ring focus:ring-blue-300"
      />
      <button
        onClick={handleSend}
        className="ml-4 px-4 py-2 bg-blue-500 text-white rounded-full shadow-md hover:bg-blue-600"
      >
        Send
      </button>
    </div>
  );
};

export default Footer;



