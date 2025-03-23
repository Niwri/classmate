'use client'

import 'react'
import Navbar from '@/components/Navbar'
import Profile from '@/public/profile.png'
import { Button } from '@mui/material'
import Image from 'next/image'
import DashboardStats from '@/components/StatBox'
import StatBox from '@/components/StatBox'
import Link from 'next/link'
import { Card, CardContent } from "@/components/ui/card";
import { useState, useEffect, useRef } from 'react'
import { useSearchParams } from 'next/navigation'
import Mascot from '@/public/mascot.png'
import Mistake from '@/public/mistake.svg'
import Correct from '@/public/checkmark.svg'

const testInfo = { "answerList": [ "x=1,y=1", "x=5", "Thereisaverticalasymptoteatx=1", "x=15Pd", "Answer is 3" ], "assignmentName": "Assignment 01", "feedbackList": [ [ 1, "Your answer (x=2, y=2) is not correct. Let's work through the equations together. The first one is 2x + 3y = 7. If we plug in your x and y values, we get 2(2) + 3(2) = 4 + 6 = 10, which is not equal to 7. The second equation, x - y = 1, will give us 2 - 2 = 0, instead of 1. The right answer is x = 1 and y = 1. Keep practicing, and remember to check your solutions in both equations!" ], [ 0, "Great effort! However, the answer you provided, 21/5, is not correct. Let's solve the equation step by step together. The equation is x + 4x = 21. First, combine like terms: x + 4x is 5x. So, we have 5x = 21. Now, to solve for x, we divide both sides by 5, which gives us x = 21/5. But when we simplify 21/5, it is equal to 4.2, not 5. The correct answer you should be looking for in decimal form is approximately 4.2, so remember to check your calculations!" ], [ 0, "Your answer is not correct. The function g(x) = x - 2 is a straight line, so it has no vertical or horizontal asymptotes. Asymptotes usually occur in rational functions (like fractions) where the graph approaches a line but never actually touches it. For g(x), it goes on forever in both directions without approaching a specific line, so there are no asymptotes. Keep practicing, and remember that asymptotes are important for functions that have some sort of restriction or behavior as they get very large or very small!" ], [ 0, "Your answer of x = -3 is not correct. Let's go through the problem together! To solve 5(3 - 2x) = -5x, we start by distributing the 5 on the left side. This gives us 15 - 10x = -5x. Then, we can add 10x to both sides to combine like terms. This gives us 15 = 5x. Finally, when we divide both sides by 5, we find that x = 3. It's easy to make a mistake, so don't worry—keep practicing!" ], [ 0, "Your answer is not correct. Let's go through the problem together! First, we need to find f(3): f(3) = 2(3) - 5 = 6 - 5 = 1. Now, let's find g(2): g(2) = 3(2) + 4 = 6 + 4 = 10. Now subtract the results: f(3) - g(2) = 1 - 10 = -9. So the correct answer is -9, not 3. Keep practicing and you'll get the hang of it!" ] ], "mistakes": 5, "questionList": [ "1. Solve the following linear systems.\\n\\na. 2x+ 3y=7\\n\\nx-y=1", "2. Solve for the variable. If there are two roots, pick the smallest.\\n\\na. x+4x=21", "3. Find the vertical and horizontal asymptotes of the following equations\\n\\na. g(x)=x-2", "4. Solve the following exponential equations:\\n\\na. 5(3 - 2x) = -5x", "5. Given the functions f(x) = 2x - 5 and g(x) = 3x + 4, evaluate the following:\\n\\na. f(3) - g(2)" ], "solutionList": [ "x=2, y=2", "21/5", "No asymptotes", "x=-3", "-9" ], "status": 1, "total": 5 }

interface DataInput {
    answerList: string[];
    assignmentName: string;
    feedbackList: (string | number)[][];
    mistakes: number;
    questionList: string[];
    solutionList: string[];
    status: number;
    total: number;
}
export default function Home() {
    const searchParams = useSearchParams()
    const [loading, setLoading] = useState(true)
    const [feedback, setFeedback] = useState<DataInput | null>(null)
    const [showFeedbacks, setShowFeedbacks] = useState<boolean[]>(new Array(5).fill(false));
    const [error, setError] = useState('')
    let name = "John Doe"

    const submitRef = useRef(false);
    const [ assignmentName, setAssignmentName ] = useState('')

    useEffect(() => {
        const submitFile = async () => {

            if (submitRef.current) return; // Skip if already submitted
            
            submitRef.current = true;
            try {
                const fileData = sessionStorage.getItem('uploadedFile');
                const filename = sessionStorage.getItem('filename');
                const assignmentid: string | null = searchParams.get('assignmentid')
                
                if (!fileData || !filename) {
                    throw new Error('No file data received');
                }
                
                // Create FormData to send file
                const formData = new FormData();
                const blob = await fetch(fileData).then(res => res.blob());
                formData.append('file', blob, filename);
                formData.append('studentId', 'student-01');
                formData.append('classroomId', 'classroom-test01');
                formData.append('assignmentId', assignmentid ? assignmentid : "");
    
                const response = await fetch('http://127.0.0.1:5000/homework/evaluate-assignment', {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'Accept': 'application/json',
                    },
                    mode: 'cors'  // Enable CORS
                });
    
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                sessionStorage.removeItem('uploadedFile');
                sessionStorage.removeItem('filename');
        
                const data = await response.json();
                //const data = testInfo
                setFeedback(data);
                setAssignmentName(data.assignmentName || "Unknown")
                setShowFeedbacks(new Array(data.answerList.length).fill(false));
                setLoading(false);
            } catch (err: any) {
                setError(err.message);
                setLoading(false);
            }
        };
    
        submitFile();
    
        // Cleanup function to revoke the URL when component unmounts
        return () => {
            const fileUrl = searchParams.get('fileUrl');
            if (fileUrl) {
                URL.revokeObjectURL(fileUrl);
            }
        };
    }, []);
    
    const toggleFeedback = (index: number) => {
        setShowFeedbacks(prev => {
            const newShowFeedbacks = [...prev];
            newShowFeedbacks[index] = !newShowFeedbacks[index];
            return newShowFeedbacks;
        });
    };

    return (
        <div className="h-screen flex flex-col">
            
            <Navbar image={Profile} name={name}/>
            <section className="flex flex-col justify-start mx-32 lg:mx-64 grow my-16">
                <Link href="/student/assignments">
                    <Button variant="contained" size="large" sx={{ 
                        borderRadius: '28px'
                    }}>
                        <h3 className="text-xl p-2">Back</h3>
                    </Button>
                </Link>
                
                <section className="mt-8 w-[80em] max-w-full flex flex-col justify-start items-center self-center grow">
                    
                    {loading ? (
                        <div className="flex justify-center items-center h-full -translate-y-[4em]">
                            <Image 
                                src={Mascot}
                                alt="Loading..." 
                                width={128} 
                                height={128} 
                                className="loading-pulse"
                            />
                        </div>
                    ) : error ? (
                        <div className="text-red-500 text-xl">{error}</div>
                    ) : (
                        <div className="w-full max-w-2xl">
                            <h2 className="text-4xl font-bold mb-8 w-full text-center">{assignmentName}</h2>
                            {feedback && (
                                <div className="my-4 flex flex-row w-full justify-around gap-x-8">
                                    <StatBox title="Correct" value={feedback.total - feedback.mistakes} progress={100 - feedback.mistakes/feedback.total * 100} subtitle="" size={1}/>
                                    <StatBox title="Mistakes" value={feedback.mistakes} progress={feedback.mistakes/feedback.total * 100} subtitle="" size={1}/>
                                </div>
                            )}
                            
                            {
                               feedback?.answerList.map((data: string, key: number) => {
                                    return (
                                        <Card key={key} className="my-8">
                                            <CardContent>
                                                <h1 className="font-bold text-2xl mb-4 flex flex-row justify-start gap-x-2 items-center">
                                                    <Image 
                                                        src={feedback.feedbackList[key][0] == 0 ? Mistake : Correct} 
                                                        alt={feedback.feedbackList[key][0] == 0 ? "Mistake" : "Correct"} 
                                                        width={32} height={32}
                                                    />
                                                    Question {key+1} 
                                                </h1>
                                                <h2 className="text-lg mb-4">
                                                    {feedback.questionList[key].replaceAll('\\n\\n', '\n').split('\n').map((line, i) => (
                                                        <span key={i}>
                                                            {line}
                                                            <br />
                                                        </span>
                                                    ))}
                                                </h2>
                                                <h2 className="text-xl">Your Answer:</h2>
                                                <p className="w-full text-center text-lg">{data}</p>
                                                {feedback.feedbackList[key][0] == 0 ? 
                                                    <>
                                                        <h2 className="text-xl mt-4">Correct Solution:</h2>
                                                        <p className="w-full text-center text-lg">{feedback.solutionList[key]}</p>
                                                    </> : <></>
                                                }
                                                <div className="flex flex-col items-center mt-4">
                                                    <Button 
                                                        variant="contained" 
                                                        onClick={() => toggleFeedback(key)}
                                                        sx={{ 
                                                            borderRadius: '28px'
                                                        }}
                                                    >
                                                        {showFeedbacks[key] ? "Close Feedback" : "Show Feedback"}
                                                    </Button>

                                                    {showFeedbacks[key] && (
                                                        <div className="mt-4 p-4 bg-gray-100 rounded-lg w-full">
                                                            <p className="text-lg whitespace-pre-wrap">{feedback.feedbackList[key][1]}</p>
                                                        </div>
                                                    )}

                                                </div>
                                            </CardContent>
                                        </Card>
                                    )
                               })
                            }
                            
                        </div>
                    )}
                </section>

            </section>

        </div>
    )
}