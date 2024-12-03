'use client'

import react from "react"
import Image from "next/image"
import LogoPng from '/public/alice/alice-2-rounded128.png'
import SvgCopy from '/public/copy.svg'


export const Main = () => {
    const [showTip, setShowTip] = react.useState(false)

    const onCopy = (e) => {
        navigator.clipboard.writeText(process.env.NEXT_PUBLIC_CA).then(() => {
            setShowTip(true)

            setTimeout(() => {
                setShowTip(false)
            }, 1000)
        })
    }

    return (
        <div className="flex flex-row justify-center items-center w-full relative">

            <button className="flex flex-row gap-1" onClick={onCopy}>
                <div className="text-xs" >
                    {process.env.NEXT_PUBLIC_CA}
                </div>

                <img src="/copy.svg" alt="copy" width="18" className="rounded-sm hover:bg-red-600" />
            </button>

            {
                showTip
                    ? <div className="absolute">
                        <div className="cyber-button-small bg-purple text-white text-sm mx-4">
                            Copied
                        </div>
                    </div>
                    : null
            }
        </div>
    )
}