import SendIcon from "./send-icon"

const InputBar = () => {
  return (
    <div className="relative">
      <input
        className="w-full px-6 py-3 border border-gray-400 rounded-full placeholder:text-gray-500"
        placeholder="Your description"
      />
      <button className="absolute top-1 right-1 bottom-1 p-2 rounded-full bg-white">
        <SendIcon />
      </button>
    </div>
  )
}

export default InputBar



