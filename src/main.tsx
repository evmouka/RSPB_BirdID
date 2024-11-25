import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import "@fontsource/nunito/300.css"
import "@fontsource/nunito/400-italic.css"
import "@fontsource/nunito/400.css"
import "@fontsource/nunito/500.css"
import "@fontsource/nunito/600.css"
import "@fontsource/nunito/700.css"
import "./index.css"
import BirdResult from "./sections/bird_result.tsx";
import Chat from "./sections/ChatLogic"
import Header from "./sections/header"
import Home from "./sections/home.tsx"

export default function App() {
    return (
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home />} />
            <Route path="chat" element={<>
                <Header />
                <Chat />
                </>} />
            <Route path="result" element={<BirdResult />} />
        </Routes>
      </BrowserRouter>
    );
  }

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);