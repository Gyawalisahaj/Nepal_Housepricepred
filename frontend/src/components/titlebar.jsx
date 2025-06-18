function TitleBar() {
  return (
    <header className=" flex flex-col bg-slate-900 text-white px-6 py-4 shadow-md items-center justify-between">
      <h1 className="text-3xl font-bold">🏠 House Price Prediction</h1>
      <nav className="w-full flex justify-end">
        <ul className="flex gap-6  text-2xl mt-14">
          <li className="hover:bg-slate-500 cursor-pointer">🛖Home</li>
          <li className="hover:bg-slate-500 cursor-pointer">ℹ️About</li>
          <li className="hover:bg-slate-500 cursor-pointer">📞Contact</li>
        </ul>
      </nav>
    </header>
  );
}

export default TitleBar;

