import  { HomeIcon, LogInIcon, PenIcon} from 'lucide-react'
import { Link } from 'react-router-dom'

export default function Navbar() {
  const navlinks = [
    {
      id: 1,
      name: "Home",
      icon: <HomeIcon/>,
      link: "/"
    },
    {
      id: 2,
      name: "Login",
      icon: <LogInIcon/>,
      link: "/login"
    },
    {
      id: 3,
      name: "Register",
      icon: <PenIcon/>,
      link: "/register"
    },
  ]
  return (
    <div className='flex justify-evenly items-center bg-slate-900 w-screen'>
        {
          navlinks.map(nav=>(
            <div className='flex gap-1 items-center p-2' key={nav.id}>
              {nav.icon}
              <Link to= {nav.link}>{nav.name}</Link>                          
            </div>
          ))
        }        
    </div>
  )
}
