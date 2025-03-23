'use client'

import 'react'
import Navbar from '@/components/Navbar'
import Profile from '@/public/profile.png'
import { Button } from '@mui/material'
import DashboardStats from '@/components/StatBox'
import StatBox from '@/components/StatBox'
import Link from 'next/link'
import { useRouter } from "next/navigation";
import { Card, CardContent } from "@/components/ui/card";
import { useState } from 'react'

export default function Page() {

    let name = "John Doe"

    const router = useRouter();

    let assignmentList = [
        {
            "name": "Assignment 1",
            "date": "March 1, 2025",
            "status": 1,
            "assignment-id": "assignment-00"
        },
        {
            "name": "Assignment 2",
            "date": "March 4, 2025",
            "status": 1,
            "assignment-id": "assignment-02"
        },
        {
            "name": "Assignment 3",
            "date": "March 22, 2025",
            "status": 0,
            "assignment-id": "assignment-01"
        }
    ]

    const [ dropFile, setDropDown ] = useState(false)
    const [ assignmentId, setAssignmentId ] = useState(0)
    const [ file, setFile ] = useState<File | null>(null);

    const handleDrop = (event: React.DragEvent<HTMLDivElement>) => {
        event.preventDefault();
        if (event.dataTransfer.files.length > 0) {
          setFile(event.dataTransfer.files[0]);
        }
    };
    
    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        if (event.target.files && event.target.files.length > 0) {
            setFile(event.target.files[0]);
        }
    };

    const isPDF = (file: File | null) => {
        return file && file.type === "application/pdf";
    };

    const handleSubmit = () => {
        if (file) {

            if (!isPDF(file)) {
                alert("Invalid file type! Please select a PDF.");
                setFile(null);
                return;
            }


            alert(`File "${file.name}" submitted!`);

            const reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onload = () => {
                const base64data = reader.result as string;
                // Store in sessionStorage
                sessionStorage.setItem('uploadedFile', base64data);
                sessionStorage.setItem('filename', file.name);
                
                // Navigate to evaluation page
                router.push(`/student/assignments/evaluate?assignmentid=${assignmentList[assignmentId]['assignment-id']}`);
            };
        } else {
          alert("No file selected!");
        }
    };

    const DropdownWindow: React.FC = () => {
        return (
            <div 
                className="absolute top-0 left-0 w-screen h-screen bg-black/30 flex flex-col items-center justify-center" 
                onClick={() => {setDropDown(false)}}
            >
                <section className="w-fit h-fit bg-white p-12 rounded-3xl flex flex-col items-center gap-y-8" onClick={(event) => event.stopPropagation()}>
                    <h1 className="font-semibold text-2xl">{assignmentList[assignmentId].name}</h1>
                    <div
                        className="w-80 h-40 border-2 border-dashed border-gray-400 rounded-lg flex items-center justify-center text-gray-600 cursor-pointer"
                        onDragOver={(event) => event.preventDefault()}
                        onDrop={handleDrop}
                        onClick={() => document.getElementById("fileInput")?.click()}
                    >
                        {file ? (
                            <p className="text-green-600">{file.name}</p>
                            ) : (
                            <p>Drag & drop a file or click to select</p>
                        )}
                    </div>

                    <input
                        id="fileInput"
                        type="file"
                        accept="application/pdf"
                        className="hidden"
                        onChange={handleFileChange}
                    />

                    <button
                        className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600"
                        onClick={handleSubmit}
                    >
                        Submit
                    </button>
                </section>
            </div>
        )
    }

    return (
        <div className="h-screen flex flex-col">
            
            <Navbar image={Profile} name={name}/>
            <section className="flex flex-col justify-start mx-64 grow my-16">
                <Link href="/student">
                    <Button variant="contained" size="large" sx={{ 
                        borderRadius: '28px'
                    }}>
                        <h3 className="text-xl p-2">Back</h3>
                    </Button>
                </Link>
                
                <section className="w-[60em] max-w-full flex flex-col justify-start items-center self-center">
                    <h1 className="text-4xl font-semibold">Assignment List</h1>

                    <table className="w-full mt-4">
                        {/* Table Headers */}
                        <thead >
                            <tr className="border border-b-4 border-x-0 border-t-0 border-gray-100 text-left">
                                <th className="px-4 py-2 w-32">Status</th>
                                <th className="px-4 py-2">Name</th>
                                <th className="px-4 py-2 w-48">Date</th>
                            </tr>
                        </thead>
                        <tbody className="">
                            <tr>
                                <td className="pt-2"></td>
                            </tr>
                            {
                                assignmentList.map((data, key) => {
                                    return (
                                        <>
                                            <tr className="text-left group cursor-pointer" onClick={() => {if(data.status == 0) {setDropDown(true); setAssignmentId(key)}}}>
                                                <td className="font-semibold px-4 py-1 w-32 rounded-l-full group-hover:bg-sky-300 flex flex-col items-center justify-center">
                                                    {data.status == 1 ? <div className="bg-green-300 rounded-full text-center w-full py-1">Complete</div> : <div className="bg-red-300 rounded-full text-center w-full py-1">Incomplete</div>}
                                                </td>
                                                <td className="px-4 py-2 group-hover:bg-sky-300 font-semibold">{data.name}</td>
                                                <td className="px-4 py-2 w-48 rounded-r-full group-hover:bg-sky-300">{data.date}</td>
                                            </tr>
                                            <tr>
                                                <td className="pt-2"></td>
                                            </tr>
                                        </>
                                    )
                                })
                            }
                        </tbody>
                    </table>
                </section>

            </section>

            {
                dropFile ? <DropdownWindow/> : <></>
            }
        </div>
    )
}