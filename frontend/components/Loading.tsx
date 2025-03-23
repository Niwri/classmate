import Image from 'next/image'
import Mascot from '@/public/mascot.png'

export default function Loading() {
    return (
        <div className="flex justify-center items-center h-full">
            <Image
            src={Mascot}
            alt="Loading..."
            width={128}
            height={128}
            className="loading-pulse"
            />
        </div>
    )
}