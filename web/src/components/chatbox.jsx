'use client'

import react from "react"
import Image from "next/image"
import SvgSend from '/public/send.svg'
import Bg1 from '/public/alice/alice-16-9-3.jpg'
import LogoPng from '/public/alice/alice-2-rounded128.png'

import AliceP1 from '/public/alice/alice-9-16-3.jpg'
import AliceP2 from '/public/alice/alice-9-16-4.jpg'
import AliceP3 from '/public/alice/alice-9-16-5.jpg'
import AliceP4 from '/public/alice/alice-9-16-6.jpg'
import AliceL1 from '/public/alice/alice-16-9-1.jpg'
import AliceL2 from '/public/alice/alice-16-9-2.jpg'
import AliceL3 from '/public/alice/alice-16-9-3.jpg'
import AliceL4 from '/public/alice/alice-16-9-4.jpg'

import Avatar1 from '/public/avatars/1.svg'
import Avatar2 from '/public/avatars/2.svg'
import Avatar3 from '/public/avatars/3.svg'
import Avatar4 from '/public/avatars/4.svg'
import Avatar5 from '/public/avatars/5.svg'
import Avatar6 from '/public/avatars/6.svg'
import Avatar7 from '/public/avatars/7.svg'
import Avatar8 from '/public/avatars/8.svg'

const BGS = {
    P: [AliceP1, AliceP2, AliceP3, AliceP4],
    L: [AliceL1, AliceL2, AliceL3, AliceL4],
}

const AVATARS = [
]

for (let i=1; i<9; i++) {
    AVATARS.push(`/avatars/${i}.svg`)
}

const apiBase = process.env.NEXT_PUBLIC_API_PATH
const post = async (url, data) => {
    try {
        const resp = await fetch(url, {
            method: 'POST',
            body: JSON.stringify(data),
            headers: {
                "Content-Type": 'application/json',
            }
        })

        if (!resp.ok) {
            throw new Error(`Response status:${resp.status}`)
        }

        return await resp.json()
    } catch (err) {
        console.log(`API exception:${err.message}`)
    }
    return {}
}

const chat = async (text) => {
    return await post(apiBase + '/chat/ask', { text })
}

const rand = (max) => {
    return Math.floor(Math.random() * max)
}

const myAvatar = AVATARS[rand(AVATARS.length)]

const MessageAvatar = ({ src }) => {
    return <img src={src} width="36" height="36" className="rounded-full bg-white" alt="" />
}

const MessagePlaceholder = () => {
    return <div className="w-28"></div>
}

// Alice's Message
const MessageAlice = ({ message }) => {
    return (
        <div className="flex flex-rol justify-start items-end gap-1">
            <MessageAvatar src="/alice/alice-2-rounded128.png" />
            <div className="oxanium-font text-md text-yellow-300">{message}</div>
            <MessagePlaceholder />
        </div>
    )
}

// My Message
const MessageMe = ({ message }) => {
    return (
        <div className="flex flex-row justify-end items-end gap-1">
            <MessagePlaceholder />
            <div className="oxanium-font text-md">{message}</div>
            <MessageAvatar src={myAvatar} />
        </div>
    )
}

export const ChatBox = ({ ...rest }) => {
    const [tobeSent, setTobeSent] = react.useState('')
    const [messages, setMessages] = react.useState([
        {
            me: false,
            text: "Welcome,I'm Alice,How are you doing today?"
        }
    ])

    const refLastMessage = react.useRef(null)

    const scrollToEnd = () => {
        refLastMessage.current?.scrollIntoView({ behavior: 'smooth' })
    }

    const onSend = () => {
        if (tobeSent.length <= 0) {
            return
        }

        messages.push({
            me: true,
            text: tobeSent,
        })

        setTobeSent('')

        chat(tobeSent).then(json => {
            console.log('json is invalid:', json)
            if (!json.reply) {
                console.log('json is invalid:', json)
                return
            }
            setMessages([...messages, {
                me: false,
                text: json.reply,
            }])

            setTimeout(() => {
                scrollToEnd()
            }, 500)
        }).catch(err => {

        })
    }

    return (
        <div className="flex-1 flex flex-col" >

            <h3 className="cyber-h mb-2">
                {`To ${process.env.NEXT_PUBLIC_APP_NAME}`}
            </h3>

            <div className="flex-1 flex flex-col relative">
                {/* bg */}
                <img src="/alice/alice-16-9-3.jpg" className="-z-10 absolute cyber-glitch-0"  style={{ 
                    objectFit: 'cover',
                    height: '100%',
                    minWidth: '100%',
                }} alt="" />

                {/* chat messages */}
                <div className="text-white oxanium-font overflow-y-scroll overflow-x-hidden scrollbar-hide" style={{
                    flex: '1 1 0',
                }}>
                    <div className="flex flex-col gap-2 p-1 whitespace-normal">
                        {
                            messages.map((msg, i) => {
                                return msg.me ? <MessageMe key={i} message={msg.text}></MessageMe>
                                    : <MessageAlice key={i} message={msg.text}></MessageAlice>
                            })
                        }
                        <div ref={refLastMessage}></div>
                    </div>
                </div>

                {/* input */}
                <div className="flex flex-row">
                    <div className="relative flex-auto pb-4">
                        <div className="cyber-input-full text-slate-50 oxanium-font flex-8">
                            <input
                                type="text"
                                placeholder="Type your message"
                                className=" placeholder-gray-200"
                                value={tobeSent}
                                onChange={e => setTobeSent(e.target.value)}
                                onKeyPress={e => {
                                    if (e.key === 'Enter') {
                                        onSend()
                                    }
                                }}
                            />
                        </div>
                    </div>

                    <button className="cyber-button-small bg-red fg-white" onClick={onSend}>
                        <span className="glitchtext"></span>
                        <span className="tag">
                            {process.env.NEXT_PUBLIC_APP_NAME}
                        </span>
                        <img src="/send.svg" width="24" alt="send" style={{
                            filter: 'invert(100%)',
                        }} />
                    </button>
                </div>
            </div>
        </div>
    )
}