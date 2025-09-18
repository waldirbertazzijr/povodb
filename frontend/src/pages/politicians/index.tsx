import React, { useState } from "react";
import { Link } from "react-router-dom";
import { usePoliticians } from "@/api/politicians";
import DebugPanel from "@/components/debug-panel";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
} from "@/components/ui/card";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";
import { ChevronRight, Search, User2 } from "lucide-react";
import { Skeleton } from "@/components/ui/skeleton";

export default function PoliticiansPage() {
    const [filters, setFilters] = useState({
        name: "",
        party: "all",
        country: "Brasil",
    });

    // Use the custom hook for politicians data
    const { data, isLoading, isError, error } = usePoliticians({
        skip: 0,
        limit: 20,
        name: filters.name || undefined,
        party: filters.party === "all" ? undefined : filters.party || undefined,
        country:
            filters.country === "all"
                ? undefined
                : filters.country || undefined,
    });

    // Debug output
    console.log("Politicians page render state:", {
        isLoading,
        isError,
        error,
        dataItems: data?.items,
        dataTotal: data?.total,
    });

    // Handle filter changes
    const handleFilterChange = (key: string, value: string) => {
        setFilters((prev) => ({ ...prev, [key]: value }));
    };

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight">
                        Políticos
                    </h1>
                    <p className="text-muted-foreground">
                        Navegue e pesquise políticos, seus registros de votação
                        e contribuições
                    </p>
                </div>
            </div>

            {/* Filters */}
            <div className="grid gap-4 md:grid-cols-3">
                <div className="relative">
                    <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
                    <Input
                        type="search"
                        placeholder="Pesquisar por nome..."
                        className="pl-8"
                        value={filters.name}
                        onChange={(e) =>
                            handleFilterChange("name", e.target.value)
                        }
                    />
                </div>
                <Select
                    value={filters.party}
                    onValueChange={(value) =>
                        handleFilterChange("party", value)
                    }
                >
                    <SelectTrigger>
                        <SelectValue placeholder="Selecionar partido" />
                    </SelectTrigger>
                    <SelectContent>
                        <SelectItem value="all">Todos os partidos</SelectItem>
                        <SelectItem value="PT">PT</SelectItem>
                        <SelectItem value="PL">PL</SelectItem>
                        <SelectItem value="MDB">MDB</SelectItem>
                        <SelectItem value="PP">PP</SelectItem>
                        <SelectItem value="PSDB">PSDB</SelectItem>
                        <SelectItem value="PSB">PSB</SelectItem>
                    </SelectContent>
                </Select>
                <Select
                    value={filters.country}
                    onValueChange={(value) =>
                        handleFilterChange("country", value)
                    }
                >
                    <SelectTrigger>
                        <SelectValue placeholder="Selecionar país" />
                    </SelectTrigger>
                    <SelectContent>
                        <SelectItem value="Brasil">Brasil</SelectItem>
                        <SelectItem value="all">Todos os países</SelectItem>
                    </SelectContent>
                </Select>
            </div>

            {/* Results */}
            {isLoading ? (
                <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                    {Array(6)
                        .fill(0)
                        .map((_, i) => (
                            <Card key={i} className="politician-card">
                                <CardHeader className="space-y-2">
                                    <Skeleton className="h-4 w-3/4" />
                                    <Skeleton className="h-4 w-1/2" />
                                </CardHeader>
                                <CardContent>
                                    <Skeleton className="h-4 w-full mb-2" />
                                    <Skeleton className="h-4 w-3/4" />
                                </CardContent>
                                <CardFooter>
                                    <Skeleton className="h-8 w-1/3" />
                                </CardFooter>
                            </Card>
                        ))}
                </div>
            ) : isError ? (
                <div className="rounded-lg border bg-card p-8 text-center">
                    <p className="text-lg font-medium">
                        Erro ao carregar políticos
                    </p>
                    <p className="text-muted-foreground mt-2">
                        Por favor, tente novamente mais tarde
                    </p>
                    <p className="text-red-500 mt-2">
                        {error instanceof Error
                            ? error.message
                            : "Erro desconhecido"}
                    </p>
                </div>
            ) : data?.items.length === 0 ? (
                <div className="rounded-lg border bg-card p-8 text-center">
                    <p className="text-lg font-medium">
                        Nenhum político encontrado
                    </p>
                    <p className="text-muted-foreground mt-2">
                        Tente ajustar seus filtros
                    </p>
                </div>
            ) : (
                <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                    {data?.items.map((politician) => (
                        <Card key={politician.id} className="politician-card">
                            <CardHeader>
                                <CardTitle>{politician.name}</CardTitle>
                                <CardDescription>
                                    {politician.party || "Independente"} •{" "}
                                    {politician.position || "Político"}
                                </CardDescription>
                            </CardHeader>
                            <CardContent>
                                <div className="flex items-center mb-2">
                                    {politician.photo_url ? (
                                        <img
                                            src={politician.photo_url}
                                            alt={politician.name}
                                            className="w-12 h-12 rounded-full mr-3 object-cover"
                                        />
                                    ) : (
                                        <div className="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center mr-3">
                                            <User2 className="h-6 w-6 text-primary" />
                                        </div>
                                    )}
                                    <div>
                                        <p>
                                            {politician.state_province},{" "}
                                            {politician.country}
                                        </p>
                                    </div>
                                </div>
                                <p className="line-clamp-2 text-sm text-muted-foreground">
                                    {politician.bio ||
                                        "Nenhuma biografia disponível."}
                                </p>
                            </CardContent>
                            <CardFooter>
                                <Link to={`/politicians/${politician.id}`}>
                                    <Button variant="ghost" size="sm">
                                        Ver detalhes{" "}
                                        <ChevronRight className="ml-1 h-4 w-4" />
                                    </Button>
                                </Link>
                            </CardFooter>
                        </Card>
                    ))}
                </div>
            )}

            {/* Pagination */}
            {data && data.total > 0 && (
                <div className="flex items-center justify-between">
                    <p className="text-sm text-muted-foreground">
                        Mostrando {data.items.length} de {data.total} políticos
                    </p>
                    <div className="flex gap-2">
                        <Button
                            variant="outline"
                            size="sm"
                            disabled={data.page <= 1}
                        >
                            Anterior
                        </Button>
                        <Button
                            variant="outline"
                            size="sm"
                            disabled={data.page >= data.pages}
                        >
                            Próximo
                        </Button>
                    </div>
                </div>
            )}

            <DebugPanel
                data={data}
                error={error instanceof Error ? error : null}
                isLoading={isLoading}
                query={`/api/v1/politicians?${new URLSearchParams({
                    skip: "0",
                    limit: "20",
                    ...(filters.name ? { name: filters.name } : {}),
                    ...(filters.party !== "all"
                        ? { party: filters.party }
                        : {}),
                    ...(filters.country !== "all"
                        ? { country: filters.country }
                        : {}),
                }).toString()}`}
            />
        </div>
    );
}
