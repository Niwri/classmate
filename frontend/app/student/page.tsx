import "react";
import Navbar from "@/components/Navbar";
import Profile from "@/public/profile.png";
import { Button } from "@mui/material";
import DashboardStats from "@/components/StatBox";
import StatBox from "@/components/StatBox";
import Link from "next/link";
import { Card, CardContent } from "@/components/ui/card";
export default function Home() {
  let name = "John Doe";
  return (
    <div className="h-screen flex flex-col">
      <Navbar image={Profile} name={name} />
      <section className="flex flex-col justify-start mx-32 md:mx-48 lg:mx-64 grow my-16">
        <section className="flex flex-row my-8 gap-x-16 justify-between">
          <StatBox
            title="To-Do"
            value={5}
            progress={36}
            subtitle={"Questions Left"}
            size={2}
          />
          <StatBox
            title="Questions Completed"
            value={11}
            progress={62}
            subtitle={"Daily Goal"}
            size={2}
          />
          <StatBox
            title="Incorrect Answers"
            value={3}
            progress={64}
            subtitle={"Incorrect Responses"}
            size={2}
          />
        </section>
        <Card className="shadow-lg rounded-2xl hover:scale-103 transition delay-1">
          <CardContent>
            <section className="w-full flex items-center justify-center my-16">
              <h1 className="text-3xl ">Welcome back, {name}!</h1>
            </section>
            <section className="flex flex-col w-full py-8 justify-center items-center">
              <Link href="/student/assignments">
                <Button
                  variant="contained"
                  size="large"
                  sx={{
                    borderRadius: "28px",
                  }}
                >
                  <h3 className="text-2xl p-4">Go to Assignments</h3>
                </Button>
              </Link>
            </section>
          </CardContent>
        </Card>
      </section>
    </div>
  );
}
