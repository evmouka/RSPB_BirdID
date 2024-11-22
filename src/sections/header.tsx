import BackIcon from "../components/back-icon"

const Header = () => {
  return (
    <header className="flex justify-center pt-4 px-6 py-3 border-b-2 shadow-sm bg-white text-xl">
      <div className="flex items-center gap-4 w-full max-w-screen-sm">
        <BackIcon />
        <h1 className="font-semibold">Chat RSPB</h1>
      </div>
    </header>
  )
}

export default Header