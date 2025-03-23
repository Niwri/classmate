import Image from "next/image";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Link from "next/link";

export default function Home() {
  return (
    <div className="flex flex-row justify-center items-center w-screen h-screen gap-x-24">
      <Link href="/teacher">
        <Button variant="contained" size="large">
          Teacher
        </Button>
      </Link>
      <Link href="/student">
        <Button variant="contained" size="large">
          Student
        </Button>
      </Link>
    </div>
  );
}
