import { Link } from "react-router-dom";
import { Menu, X, Search, Sun, Moon } from "lucide-react";
import { useTheme } from "@/components/theme-provider";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import {
    NavigationMenu,
    NavigationMenuContent,
    NavigationMenuItem,
    NavigationMenuLink,
    NavigationMenuList,
    NavigationMenuTrigger,
    navigationMenuTriggerStyle,
} from "@/components/ui/navigation-menu";

interface NavbarProps {
    setSidebarOpen: (open: boolean) => void;
}

export default function Navbar({ setSidebarOpen }: NavbarProps) {
    const { theme, setTheme } = useTheme();

    return (
        <header className="sticky top-0 z-40 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
            <div className="container flex h-16 items-center justify-between">
                <div className="flex items-center">
                    <Button
                        variant="ghost"
                        className="mr-2 px-2 md:hidden"
                        onClick={() => setSidebarOpen(true)}
                    >
                        <Menu className="h-5 w-5" />
                        <span className="sr-only">Open sidebar</span>
                    </Button>
                    <Link to="/" className="flex items-center space-x-2">
                        <span className="text-xl font-bold tracking-tight">
                            PovoDB
                        </span>
                    </Link>
                    <div className="hidden md:flex md:items-center md:space-x-4 md:ml-6">
                        <NavigationMenu>
                            <NavigationMenuList>
                                <NavigationMenuItem>
                                    <NavigationMenuLink
                                        className={navigationMenuTriggerStyle()}
                                        onClick={() =>
                                            (window.location.href =
                                                "/politicians")
                                        }
                                    >
                                        Políticos
                                    </NavigationMenuLink>
                                </NavigationMenuItem>
                                <NavigationMenuItem>
                                    <NavigationMenuLink
                                        className={navigationMenuTriggerStyle()}
                                        onClick={() =>
                                            (window.location.href = "/bills")
                                        }
                                    >
                                        Projetos
                                    </NavigationMenuLink>
                                </NavigationMenuItem>
                                <NavigationMenuItem>
                                    <NavigationMenuLink
                                        className={navigationMenuTriggerStyle()}
                                        onClick={() =>
                                            (window.location.href = "/votes")
                                        }
                                    >
                                        Votações
                                    </NavigationMenuLink>
                                </NavigationMenuItem>
                                <NavigationMenuItem>
                                    <NavigationMenuLink
                                        className={navigationMenuTriggerStyle()}
                                        onClick={() =>
                                            (window.location.href =
                                                "/contributions")
                                        }
                                    >
                                        Contribuições
                                    </NavigationMenuLink>
                                </NavigationMenuItem>
                            </NavigationMenuList>
                        </NavigationMenu>
                    </div>
                </div>
                <div className="flex items-center space-x-2">
                    <div className="relative rounded-md shadow-sm">
                        <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                            <Search
                                className="h-4 w-4 text-gray-400"
                                aria-hidden="true"
                            />
                        </div>
                        <input
                            type="text"
                            className="block w-full rounded-md border-0 py-1.5 pl-10 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary sm:text-sm sm:leading-6"
                            placeholder="Pesquisar..."
                        />
                    </div>
                    <Button
                        variant="ghost"
                        size="icon"
                        onClick={() =>
                            setTheme(theme === "dark" ? "light" : "dark")
                        }
                    >
                        {theme === "dark" ? (
                            <Sun className="h-5 w-5" />
                        ) : (
                            <Moon className="h-5 w-5" />
                        )}
                        <span className="sr-only">Toggle theme</span>
                    </Button>
                </div>
            </div>
        </header>
    );
}
