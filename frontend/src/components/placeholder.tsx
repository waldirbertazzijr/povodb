import React from "react";
import { Link } from "react-router-dom";
import { ArrowLeft, Construction } from "lucide-react";
import { Button } from "@/components/ui/button";

interface PlaceholderProps {
    title?: string;
    description?: string;
    returnPath?: string;
    returnLabel?: string;
    icon?: React.ReactNode;
}

export default function Placeholder({
    title = "Página em Construção",
    description = "Este recurso está sendo desenvolvido e estará disponível em breve.",
    returnPath = "/",
    returnLabel = "Voltar para Início",
    icon = <Construction className="h-12 w-12 text-primary" />,
}: PlaceholderProps) {
    return (
        <div className="flex flex-col items-center justify-center min-h-[60vh] text-center px-4">
            <div className="mb-6">{icon}</div>
            <h1 className="text-3xl font-bold mb-4">{title}</h1>
            <p className="text-lg text-muted-foreground max-w-[500px] mb-8">
                {description}
            </p>
            <Link to={returnPath}>
                <Button>
                    <ArrowLeft className="mr-2 h-4 w-4" />
                    {returnLabel}
                </Button>
            </Link>
        </div>
    );
}
