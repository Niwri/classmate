import { Card, CardContent } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { PieChart, Pie, Cell } from "recharts";

interface StatBoxProps {
  title: string;
  value: number;
  progress: number;
  subtitle: string;
  size: number | 2;
}

const data = [
  { name: "Completed", value: 62 },
  { name: "Remaining", value: 38 },
];

const COLORS = ["#4A90E2", "#D9E8F5"];

const StatBox: React.FC<StatBoxProps> = ({
  title,
  value,
  progress,
  subtitle,
  size,
}) => {
  let width = 96;
  if (size == 1) width = 64;
  else if (size == 0) width = 32;
  return (
    <Card
      className={
        "p-4 w-" +
        width +
        " shadow-lg rounded-2xl hover:scale-110 transition delay-1"
      }
    >
      <CardContent className="flex flex-col items-left">
        <span className="w-64 w-96 w-32 h-0"></span>
        <h2 className="text-xl font-semibold">{title}</h2>
        <p className="text-4xl font-bold">{value}</p>
        <Progress
          value={progress}
          className="w-full my-2 [&>div]:bg-sky-500 bg-sky-200"
        />
        <p className="text-sm text-gray-600 font-semibold self-center">
          {subtitle}
        </p>
      </CardContent>
    </Card>
  );
};

export default StatBox;
