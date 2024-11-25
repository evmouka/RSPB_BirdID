import { ReactNode } from "react"
import Sender from "../types/sender"
import RspbIcon from "./rspb-icon"
import UserIcon from "./user-icon"

interface ChatBubbleCustomisation {
  direction: string
  icon: ReactNode
  styles: string
  title: string
}

const SenderCustomisation: { [sender in Sender]: ChatBubbleCustomisation } = {
  chatbot: {
    direction: "flex-row",
    icon: <RspbIcon />,
    styles: "rounded-tl bg-white",
    title: "Chat RSPB",
  },
  user: {
    direction: "flex-row-reverse",
    icon: <UserIcon />,
    styles: "rounded-tr bg-teal-900 text-white",
    title: "You",
  },
}

interface ChatBubbleProps {
  sender: Sender
  content: string
}

const ChatBubble = ({ sender, content }: ChatBubbleProps) => {
  return (
    <div className={`flex ${SenderCustomisation[sender].direction} gap-2`}>
      <div className="shrink-0">{SenderCustomisation[sender].icon}</div>
      <div className={`p-4 rounded-xl ${SenderCustomisation[sender].styles}`}>
        <h2 className="opacity-75 text-sm uppercase">{SenderCustomisation[sender].title}</h2>
        <p>{content}</p>
      </div>
    </div>
  )
}

export default ChatBubble
