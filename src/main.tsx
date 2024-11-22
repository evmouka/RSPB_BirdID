import { createRoot } from "react-dom/client"
import App from "./app.tsx"
import "@fontsource/nunito/300.css"
import "@fontsource/nunito/400-italic.css"
import "@fontsource/nunito/400.css"
import "@fontsource/nunito/500.css"
import "@fontsource/nunito/600.css"
import "@fontsource/nunito/700.css"
import "./index.css"

createRoot(document.getElementById("root")!).render(<App />)

