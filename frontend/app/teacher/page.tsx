import "react";
import Navbar from "@/components/Navbar";
import Profile from "@/public/profile.png";

export default function Home() {
  let name = "Mrs. T";
  return (
    <div>
      <Navbar image={Profile} name={name} />
    </div>
  );
}
