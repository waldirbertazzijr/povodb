import React from "react";
import { Link, useLocation } from "react-router-dom";
import { X, BarChart3, FileText, Users, DollarSign, Home } from "lucide-react";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";

interface SidebarProps {
    open: boolean;
    setOpen: (open: boolean) => void;
}

export default function Sidebar({ open, setOpen }: SidebarProps) {
    const location = useLocation();

    const navItems = [
        { href: "/", label: "Início", icon: Home },
        { href: "/politicians", label: "Políticos", icon: Users },
        { href: "/bills", label: "Projetos", icon: FileText },
        { href: "/votes", label: "Votações", icon: BarChart3 },
        { href: "/contributions", label: "Contribuições", icon: DollarSign },
    ];

    return (
        <>
            {/* Mobile sidebar backdrop */}
            {open && (
                <div
                    className="fixed inset-0 z-40 bg-background/80 backdrop-blur-sm md:hidden"
                    onClick={() => setOpen(false)}
                />
            )}

            {/* Sidebar */}
            <aside
                className={cn(
                    "fixed inset-y-0 left-0 z-50 w-72 border-r bg-background transition-transform duration-300 md:sticky md:transition-none",
                    open
                        ? "translate-x-0"
                        : "-translate-x-full md:translate-x-0",
                )}
            >
                <div className="flex h-16 items-center justify-between border-b px-4">
                    <Link to="/" className="flex items-center">
                        <span className="text-xl font-bold tracking-tight">
                            PovoDB
                        </span>
                    </Link>
                    <Button
                        variant="ghost"
                        size="icon"
                        className="md:hidden"
                        onClick={() => setOpen(false)}
                    >
                        <X className="h-5 w-5" />
                        <span className="sr-only">Fechar menu</span>
                    </Button>
                </div>
                <nav className="flex flex-col gap-1 p-4">
                    {navItems.map((item) => {
                        const isActive =
                            location.pathname === item.href ||
                            (item.href !== "/" &&
                                location.pathname.startsWith(item.href));

                        return (
                            <Link
                                key={item.href}
                                to={item.href}
                                className={cn(
                                    "flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium transition-colors",
                                    isActive
                                        ? "bg-primary text-primary-foreground"
                                        : "hover:bg-muted",
                                )}
                                onClick={() => setOpen(false)}
                            >
                                <item.icon className="h-4 w-4" />
                                {item.label}
                            </Link>
                        );
                    })}
                </nav>
            </aside>
        </>
    );
}
