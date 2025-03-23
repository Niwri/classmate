"use client";

import Image from "next/image";

export default function Navbar({image, name}: {image: any | null, name: string}) {
    return (
        <div className="flex flex-row justify-between px-32 mt-16">
            <h1 className="text-4xl font-bold">ClassMate</h1>
            <div className="flex flex-row gap-x-8 items-center justify-end">
                <h3 className="text-3xl font-medium">{name}</h3>
                <Image width={75} height={75} src={image} alt="Profile Picture"/>
            </div>
        </div>
    )
}