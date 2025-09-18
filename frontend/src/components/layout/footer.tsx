import React from "react";
import { Link } from "react-router-dom";

export default function Footer() {
    const currentYear = new Date().getFullYear();

    return (
        <footer className="border-t py-6 md:py-0">
            <div className="container flex flex-col items-center justify-between gap-4 md:h-16 md:flex-row">
                <p className="text-center text-sm leading-loose text-muted-foreground md:text-left">
                    &copy; {currentYear} PovoDB. Todos os direitos reservados.
                </p>
                <div className="flex items-center gap-4">
                    <Link
                        to="/about"
                        className="text-sm font-medium text-muted-foreground transition-colors hover:text-foreground"
                    >
                        Sobre
                    </Link>
                    <Link
                        to="/privacy"
                        className="text-sm font-medium text-muted-foreground transition-colors hover:text-foreground"
                    >
                        Privacidade
                    </Link>
                    <Link
                        to="/terms"
                        className="text-sm font-medium text-muted-foreground transition-colors hover:text-foreground"
                    >
                        Termos
                    </Link>
                    <a
                        href="https://github.com/yourusername/povodb"
                        target="_blank"
                        rel="noreferrer"
                        className="text-sm font-medium text-muted-foreground transition-colors hover:text-foreground"
                    >
                        GitHub
                    </a>
                </div>
            </div>
        </footer>
    );
}
