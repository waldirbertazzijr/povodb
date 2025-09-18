import React from "react";
import { useParams, Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import {
    ArrowLeft,
    Calendar,
    Coins,
    Vote,
    FileText,
    Users,
    ExternalLink,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { getPolitician, getPoliticianWithRelations } from "@/api/politicians";
import { formatCurrency, formatDate } from "@/lib/utils";
import Placeholder from "@/components/placeholder";
import DebugPanel from "@/components/debug-panel";

export default function PoliticianDetailsPage() {
    const { id } = useParams<{ id: string }>();

    const {
        data: politician,
        isLoading,
        isError,
        error,
    } = useQuery({
        queryKey: ["politician", id],
        queryFn: () => {
            console.log("Fetching politician details for ID:", id);
            return getPoliticianWithRelations(id!)
                .then((data) => {
                    console.log("Politician details response:", data);
                    return data;
                })
                .catch((err) => {
                    console.error("Error fetching politician details:", err);
                    throw err;
                });
        },
        enabled: !!id,
        retry: 1,
    });

    if (isLoading) {
        return (
            <div className="space-y-4">
                <div className="animate-pulse h-8 w-48 bg-muted rounded mb-4"></div>
                <div className="grid gap-4 md:grid-cols-2">
                    <div className="animate-pulse h-64 bg-muted rounded"></div>
                    <div className="space-y-2">
                        <div className="animate-pulse h-6 w-3/4 bg-muted rounded"></div>
                        <div className="animate-pulse h-6 w-1/2 bg-muted rounded"></div>
                        <div className="animate-pulse h-6 w-5/6 bg-muted rounded"></div>
                        <div className="animate-pulse h-6 w-4/5 bg-muted rounded"></div>
                    </div>
                </div>
            </div>
        );
    }

    if (isError || !politician) {
        return (
            <div className="rounded-lg border bg-card p-8 text-center">
                <p className="text-lg font-medium">
                    Error loading politician details
                </p>
                <p className="text-muted-foreground mt-2">
                    Could not find the requested politician
                </p>
                <Link to="/politicians" className="mt-4 inline-block">
                    <Button>
                        <ArrowLeft className="mr-2 h-4 w-4" />
                        Back to Politicians
                    </Button>
                </Link>
            </div>
        );
    }

    return (
        <>
            <div className="space-y-6">
                <div className="flex items-center gap-2">
                    <Link to="/politicians">
                        <Button variant="ghost" size="sm">
                            <ArrowLeft className="mr-1 h-4 w-4" />
                            Voltar
                        </Button>
                    </Link>
                    <h1 className="text-3xl font-bold tracking-tight">
                        {politician.name}
                    </h1>
                </div>

                <div className="grid gap-6 md:grid-cols-3">
                    <div className="space-y-4">
                        <Card>
                            <CardHeader>
                                <CardTitle>Perfil</CardTitle>
                            </CardHeader>
                            <CardContent className="space-y-4">
                                <div className="flex flex-col items-center gap-2 text-center">
                                    {politician.photo_url ? (
                                        <img
                                            src={politician.photo_url}
                                            alt={politician.name}
                                            className="w-32 h-32 rounded-full object-cover mb-2"
                                        />
                                    ) : (
                                        <div className="w-32 h-32 rounded-full bg-primary/10 flex items-center justify-center mb-2">
                                            <Users className="h-16 w-16 text-primary" />
                                        </div>
                                    )}
                                    <h2 className="text-xl font-bold">
                                        {politician.name}
                                    </h2>
                                    <p className="text-muted-foreground">
                                        {politician.party || "Independent"}
                                    </p>
                                    <p className="text-muted-foreground">
                                        {politician.position || "Politician"}
                                    </p>
                                </div>

                                <div className="space-y-2">
                                    <div className="flex justify-between">
                                        <span className="text-muted-foreground">
                                            Localização:
                                        </span>
                                        <span>
                                            {politician.state_province},{" "}
                                            {politician.country}
                                        </span>
                                    </div>
                                    {politician.website && (
                                        <div className="flex justify-between">
                                            <span className="text-muted-foreground">
                                                Website:
                                            </span>
                                            <a
                                                href={politician.website}
                                                target="_blank"
                                                rel="noopener noreferrer"
                                                className="text-primary hover:underline flex items-center"
                                            >
                                                Visitar{" "}
                                                <ExternalLink className="ml-1 h-3 w-3" />
                                            </a>
                                        </div>
                                    )}
                                    <div className="flex justify-between">
                                        <span className="text-muted-foreground">
                                            Adicionado:
                                        </span>
                                        <span>
                                            {formatDate(politician.created_at)}
                                        </span>
                                    </div>
                                </div>
                            </CardContent>
                        </Card>

                        <Card>
                            <CardHeader>
                                <CardTitle>Biografia</CardTitle>
                            </CardHeader>
                            <CardContent>
                                <p className="text-sm">
                                    {politician.bio ||
                                        "Nenhuma biografia disponível para este político."}
                                </p>
                            </CardContent>
                        </Card>
                    </div>

                    <div className="md:col-span-2">
                        <Tabs defaultValue="votes">
                            <TabsList className="grid w-full grid-cols-3">
                                <TabsTrigger value="votes">
                                    <Vote className="mr-2 h-4 w-4" />
                                    Votações
                                </TabsTrigger>
                                <TabsTrigger value="bills">
                                    <FileText className="mr-2 h-4 w-4" />
                                    Projetos
                                </TabsTrigger>
                                <TabsTrigger value="contributions">
                                    <Coins className="mr-2 h-4 w-4" />
                                    Contribuições
                                </TabsTrigger>
                            </TabsList>
                            <TabsContent value="votes" className="mt-4">
                                {politician.votes &&
                                politician.votes.length > 0 ? (
                                    <div className="space-y-4">
                                        {politician.votes.map((vote: any) => (
                                            <Card key={vote.id}>
                                                <CardContent className="p-4">
                                                    <div className="flex justify-between items-start gap-4">
                                                        <div>
                                                            <h3 className="font-medium">
                                                                {
                                                                    vote.bill_title
                                                                }
                                                            </h3>
                                                            <div className="flex items-center text-sm text-muted-foreground mt-1">
                                                                <Calendar className="mr-1 h-3 w-3" />
                                                                <span>
                                                                    {formatDate(
                                                                        vote.vote_date,
                                                                    )}
                                                                </span>
                                                            </div>
                                                        </div>
                                                        <div
                                                            className={`px-2 py-1 rounded-full text-xs font-medium ${
                                                                vote.vote_position ===
                                                                "sim"
                                                                    ? "vote-yea"
                                                                    : vote.vote_position ===
                                                                        "não"
                                                                      ? "vote-nay"
                                                                      : "vote-neutral"
                                                            }`}
                                                        >
                                                            {vote.vote_position}
                                                        </div>
                                                    </div>
                                                    <div className="mt-2 text-sm">
                                                        <span className="text-muted-foreground">
                                                            Resultado:
                                                        </span>{" "}
                                                        {vote.vote_result}
                                                    </div>
                                                </CardContent>
                                            </Card>
                                        ))}
                                    </div>
                                ) : (
                                    <div className="text-center py-8 text-muted-foreground">
                                        Nenhum registro de votação disponível
                                        para este político.
                                    </div>
                                )}
                            </TabsContent>
                            <TabsContent value="bills" className="mt-4">
                                {politician.sponsored_bills &&
                                politician.sponsored_bills.length > 0 ? (
                                    <div className="space-y-4">
                                        {politician.sponsored_bills.map(
                                            (bill: any) => (
                                                <Card key={bill.id}>
                                                    <CardContent className="p-4">
                                                        <div>
                                                            <h3 className="font-medium">
                                                                {bill.title}
                                                            </h3>
                                                            <div className="flex items-center gap-2 mt-1">
                                                                <span className="text-xs bg-primary/10 text-primary px-2 py-0.5 rounded-full">
                                                                    {
                                                                        bill.bill_number
                                                                    }
                                                                </span>
                                                                {bill.introduced_date && (
                                                                    <span className="text-xs text-muted-foreground">
                                                                        Apresentado:{" "}
                                                                        {formatDate(
                                                                            bill.introduced_date,
                                                                        )}
                                                                    </span>
                                                                )}
                                                                <span className="text-xs bg-secondary/10 text-secondary-foreground px-2 py-0.5 rounded-full">
                                                                    {bill.status ||
                                                                        "Status desconhecido"}
                                                                </span>
                                                            </div>
                                                        </div>
                                                        {bill.description && (
                                                            <p className="mt-2 text-sm text-muted-foreground">
                                                                {
                                                                    bill.description
                                                                }
                                                            </p>
                                                        )}
                                                    </CardContent>
                                                </Card>
                                            ),
                                        )}
                                    </div>
                                ) : (
                                    <div className="text-center py-8 text-muted-foreground">
                                        Nenhum projeto patrocinado disponível
                                        para este político.
                                    </div>
                                )}
                            </TabsContent>
                            <TabsContent value="contributions" className="mt-4">
                                {politician.contributions &&
                                politician.contributions.length > 0 ? (
                                    <div className="space-y-4">
                                        {politician.contributions.map(
                                            (contribution: any) => (
                                                <Card key={contribution.id}>
                                                    <CardContent className="p-4">
                                                        <div className="flex justify-between items-start">
                                                            <div>
                                                                <h3 className="font-medium">
                                                                    {
                                                                        contribution.contributor_name
                                                                    }
                                                                </h3>
                                                                <div className="flex items-center text-sm text-muted-foreground mt-1">
                                                                    <Coins className="mr-1 h-3 w-3" />
                                                                    <span>
                                                                        {formatCurrency(
                                                                            contribution.amount,
                                                                        )}
                                                                    </span>
                                                                    <span className="mx-1">
                                                                        •
                                                                    </span>
                                                                    <Calendar className="mr-1 h-3 w-3" />
                                                                    <span>
                                                                        {formatDate(
                                                                            contribution.contribution_date,
                                                                        )}
                                                                    </span>
                                                                </div>
                                                            </div>
                                                            {contribution.contributor_type && (
                                                                <div className="px-2 py-1 rounded-full text-xs font-medium bg-secondary/10 text-secondary-foreground">
                                                                    {
                                                                        contribution.contributor_type
                                                                    }
                                                                </div>
                                                            )}
                                                        </div>
                                                    </CardContent>
                                                </Card>
                                            ),
                                        )}
                                    </div>
                                ) : (
                                    <div className="text-center py-8 text-muted-foreground">
                                        Nenhum registro de contribuição
                                        disponível para este político.
                                    </div>
                                )}
                            </TabsContent>
                        </Tabs>
                    </div>
                </div>
            </div>
            <DebugPanel
                data={politician}
                error={error instanceof Error ? error : null}
                isLoading={isLoading}
                query={`/api/v1/politicians/${id}/details`}
            />
        </>
    );
}
