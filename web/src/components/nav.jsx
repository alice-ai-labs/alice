
import Image from "next/image"
import Link from "next/link"
import LogoPng from '/public/alice/alice-2-rounded128.png'
import LogoDexscreener from '/public/dexscreener.svg'
import LogoGmgn from '/public/gmgn.svg'
import LogoPumpfun from '/public/pumpfun.webp'


const NAV_BTNS = [
    {
        icon: '/pumpfun.webp',
        url: 'https://google.com',
        name: '',
    }, {
        icon: '/dexscreener.svg',
        url: 'https://google.com',
        name: '',
    }, {
        icon: 'https://upload.wikimedia.org/wikipedia/commons/5/53/X_logo_2023_original.svg',
        url: 'https://google.com',
        name: '',
        invert: true,
    }, {
        icon: 'https://upload.wikimedia.org/wikipedia/commons/6/62/Telegram_logo_icon.svg',
        url: 'https://google.com',
        name: '',
    }, {
        icon: 'https://upload.wikimedia.org/wikipedia/commons/c/c2/GitHub_Invertocat_Logo.svg',
        url: 'https://google.com',
        name: '',
        invert: true,
    }
]


const IconButton = ({ url, src, alt = '', invert = false }) => {

    return (
        <div className="flex flex-row items-center px-2">
            <Link href={url}>
                <img src={src} alt={alt} width="18" height="18" className={invert ? 'invert' : null} />
            </Link>
        </div>
    )
}

export const Nav = () => {

    return (
        <div className="flex flex-row justify-between bg-black flex-nowrap fg-white cyber-razor-bottom">
            <div className="cyberpunk-font-og text-2xl lg:text-4xl">
                <Link href={process.env.NEXT_PUBLIC_APP_DOMAIN}>
                    {process.env.NEXT_PUBLIC_APP_NAME}
                </Link>
            </div>

            <div className="flex flex-row justify-space-between items-center">
                {
                    NAV_BTNS.map((btn, i) => {
                        return <IconButton key={i} url={btn.url} src={btn.icon} alt={btn.name} invert={btn.invert} />
                    })
                }
            </div>
        </div>
    )
}