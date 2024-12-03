
import { Nav } from "../components/nav";
import { Main } from "../components/main";
import { ChatBox } from "../components/chatbox";

export default function Home() {
  return (
    <div className="absolute top-0 right-0 bottom-0 left-0 flex flex-col max-h-screen lg:px-40">
      <Nav></Nav>
      <Main></Main>
      <ChatBox></ChatBox>
    </div>
  );
}
