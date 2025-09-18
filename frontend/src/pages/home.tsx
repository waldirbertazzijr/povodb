import React from "react";
import { Link } from "react-router-dom";
import {
    ArrowRight,
    BarChart3,
    FileText,
    Users,
    DollarSign,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
} from "@/components/ui/card";

export default function HomePage() {
    return (
        <div className="space-y-8">
            <section className="py-12 md:py-16 lg:py-20">
                <div className="container px-4 md:px-6">
                    <div className="flex flex-col items-center justify-center space-y-4 text-center">
                        <div className="space-y-2">
                            <h1 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl">
                                PovoDB: Plataforma de Transparência Política
                            </h1>
                            <p className="mx-auto max-w-[700px] text-gray-500 md:text-xl dark:text-gray-400">
                                Acompanhe políticos, projetos de lei, votações e
                                contribuições financeiras para trazer
                                transparência à política brasileira.
                            </p>
                        </div>
                        <div className="flex flex-col gap-2 min-[400px]:flex-row">
                            <Link to="/politicians">
                                <Button>
                                    Ver Políticos{" "}
                                    <ArrowRight className="ml-2 h-4 w-4" />
                                </Button>
                            </Link>
                            <Link to="/bills">
                                <Button variant="outline">
                                    Explorar Projetos{" "}
                                    <ArrowRight className="ml-2 h-4 w-4" />
                                </Button>
                            </Link>
                        </div>
                    </div>
                </div>
            </section>

            <section className="py-8 md:py-12">
                <div className="container px-4 md:px-6">
                    <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
                        <Card className="transition-all hover:shadow-md">
                            <CardHeader className="pb-2">
                                <div className="p-2 bg-primary/10 w-fit rounded-md mb-2">
                                    <Users className="h-6 w-6 text-primary" />
                                </div>
                                <CardTitle>Políticos</CardTitle>
                                <CardDescription>
                                    Informações detalhadas sobre políticos, seus
                                    cargos e afiliações partidárias.
                                </CardDescription>
                            </CardHeader>
                            <CardContent className="pb-2 text-2xl font-bold">
                                Dados de perfil para centenas de políticos
                                brasileiros
                            </CardContent>
                            <CardFooter>
                                <Link
                                    to="/politicians"
                                    className="text-primary hover:underline inline-flex items-center"
                                >
                                    Ver Políticos{" "}
                                    <ArrowRight className="ml-1 h-4 w-4" />
                                </Link>
                            </CardFooter>
                        </Card>

                        <Card className="transition-all hover:shadow-md">
                            <CardHeader className="pb-2">
                                <div className="p-2 bg-primary/10 w-fit rounded-md mb-2">
                                    <FileText className="h-6 w-6 text-primary" />
                                </div>
                                <CardTitle>Projetos de Lei</CardTitle>
                                <CardDescription>
                                    Acompanhe a legislação, incluindo autores,
                                    status e histórico de votações.
                                </CardDescription>
                            </CardHeader>
                            <CardContent className="pb-2 text-2xl font-bold">
                                Acompanhamento e análise abrangente de projetos
                                de lei
                            </CardContent>
                            <CardFooter>
                                <Link
                                    to="/bills"
                                    className="text-primary hover:underline inline-flex items-center"
                                >
                                    Ver Projetos{" "}
                                    <ArrowRight className="ml-1 h-4 w-4" />
                                </Link>
                            </CardFooter>
                        </Card>

                        <Card className="transition-all hover:shadow-md">
                            <CardHeader className="pb-2">
                                <div className="p-2 bg-primary/10 w-fit rounded-md mb-2">
                                    <BarChart3 className="h-6 w-6 text-primary" />
                                </div>
                                <CardTitle>Votações</CardTitle>
                                <CardDescription>
                                    Veja como os políticos votam em legislações
                                    importantes.
                                </CardDescription>
                            </CardHeader>
                            <CardContent className="pb-2 text-2xl font-bold">
                                Transparência nos registros de votação
                            </CardContent>
                            <CardFooter>
                                <Link
                                    to="/votes"
                                    className="text-primary hover:underline inline-flex items-center"
                                >
                                    Ver Votações{" "}
                                    <ArrowRight className="ml-1 h-4 w-4" />
                                </Link>
                            </CardFooter>
                        </Card>

                        <Card className="transition-all hover:shadow-md">
                            <CardHeader className="pb-2">
                                <div className="p-2 bg-primary/10 w-fit rounded-md mb-2">
                                    <DollarSign className="h-6 w-6 text-primary" />
                                </div>
                                <CardTitle>Contribuições</CardTitle>
                                <CardDescription>
                                    Explore as contribuições financeiras para
                                    campanhas políticas.
                                </CardDescription>
                            </CardHeader>
                            <CardContent className="pb-2 text-2xl font-bold">
                                Siga o dinheiro na política brasileira
                            </CardContent>
                            <CardFooter>
                                <Link
                                    to="/contributions"
                                    className="text-primary hover:underline inline-flex items-center"
                                >
                                    Ver Contribuições{" "}
                                    <ArrowRight className="ml-1 h-4 w-4" />
                                </Link>
                            </CardFooter>
                        </Card>
                    </div>
                </div>
            </section>

            <section className="py-8 md:py-12 bg-muted/50">
                <div className="container px-4 md:px-6">
                    <div className="flex flex-col items-center justify-center space-y-4 text-center">
                        <div className="space-y-2">
                            <h2 className="text-2xl font-bold tracking-tighter sm:text-3xl">
                                Trazendo Transparência para a Política
                            </h2>
                            <p className="mx-auto max-w-[700px] text-gray-500 md:text-lg dark:text-gray-400">
                                PovoDB ajuda os cidadãos a entender os processos
                                políticos, acompanhar registros de votação e
                                monitorar as influências financeiras nas
                                decisões políticas brasileiras.
                            </p>
                        </div>
                        <div className="mx-auto w-full max-w-sm space-y-2">
                            <div className="flex justify-center">
                                <Link to="/politicians">
                                    <Button variant="default">
                                        Começar{" "}
                                        <ArrowRight className="ml-2 h-4 w-4" />
                                    </Button>
                                </Link>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
        </div>
    );
}
