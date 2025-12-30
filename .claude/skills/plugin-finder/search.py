#!/usr/bin/env python3
"""Plugin registry search tool - filters plugins by tags without loading full JSON into LLM context."""

import json
import argparse
from pathlib import Path

REGISTRY_PATH = Path(__file__).parent / "data" / "registry.json"
MARKETPLACES_PATH = Path(__file__).parent / "data" / "marketplaces.json"

def load_registry():
    with open(REGISTRY_PATH) as f:
        return json.load(f)

def load_marketplaces():
    with open(MARKETPLACES_PATH) as f:
        return json.load(f)

def format_marketplaces(marketplaces, verbose=False):
    """Format marketplaces for display."""
    if not marketplaces:
        return "No marketplaces found."

    lines = []
    for m in marketplaces:
        if verbose:
            stars = f" ({m['stars']}★)" if m.get("stars") else ""
            lines.append(f"{m['name']}{stars} [{m.get('type')}]")
            lines.append(f"  {m.get('description', 'No description')}")
            lines.append(f"  URL: {m.get('url')}")
            lines.append(f"  Status: {m.get('status')} | Last push: {m.get('lastPush', 'unknown')}")
            if m.get("pluginCount"):
                lines.append(f"  Plugin count: {m['pluginCount']}")
            if m.get("notes"):
                lines.append(f"  Notes: {m['notes']}")
            lines.append("")
        else:
            stars = f" {m['stars']}★" if m.get("stars") else ""
            lines.append(f"{m['name']:35} {m.get('type',''):12} {m.get('status',''):10}{stars}")

    return "\n".join(lines)

def get_all_plugins(registry):
    """Flatten internal and external plugins into one list."""
    plugins = []
    for plugin in registry["plugins"].get("internal", []):
        plugin["source"] = "internal"
        plugins.append(plugin)
    for plugin in registry["plugins"].get("external", []):
        plugin["source"] = "external"
        plugins.append(plugin)
    return plugins

def filter_plugins(plugins, **filters):
    """Filter plugins by provided criteria."""
    results = plugins

    if filters.get("tier"):
        results = [p for p in results if p.get("qualityTier") == filters["tier"]]

    if filters.get("category"):
        results = [p for p in results if p.get("category") == filters["category"]]

    if filters.get("provider"):
        results = [p for p in results if p.get("providerTier") == filters["provider"]]

    if filters.get("type"):
        results = [p for p in results if filters["type"] in p.get("componentTypes", [])]

    if filters.get("usecase"):
        results = [p for p in results if filters["usecase"] in p.get("useCases", [])]

    if filters.get("framework"):
        results = [p for p in results if filters["framework"] in p.get("frameworks", [])]

    if filters.get("search"):
        term = filters["search"].lower()
        results = [p for p in results if
                   term in p.get("name", "").lower() or
                   term in p.get("description", "").lower()]

    return results

def format_output(plugins, verbose=False):
    """Format plugins for display."""
    if not plugins:
        return "No plugins found matching criteria."

    lines = []
    for p in plugins:
        if verbose:
            stars = f" ({p['stars']}★)" if p.get("stars") else ""
            types = ",".join(p.get("componentTypes", []))
            lines.append(f"{p['name']}{stars} [{p.get('category')}] [{types}]")
            lines.append(f"  {p.get('description', 'No description')}")
            lines.append(f"  Tier: {p.get('qualityTier')} | Provider: {p.get('providerTier')}")
            if p.get("useCases"):
                lines.append(f"  Use cases: {', '.join(p['useCases'])}")
            lines.append("")
        else:
            stars = f" {p['stars']}★" if p.get("stars") else ""
            lines.append(f"{p['name']:25} {p.get('qualityTier',''):8} {p.get('category',''):15}{stars}")

    return "\n".join(lines)

def list_values(registry, field):
    """List all unique values for a field."""
    if field == "categories":
        return list(registry["schema"]["categories"].keys())
    elif field == "types":
        return list(registry["schema"]["componentTypes"].keys())
    elif field == "providers":
        return list(registry["schema"]["providerTiers"].keys())
    elif field == "tiers":
        return list(registry["schema"]["qualityTiers"].keys())
    elif field == "usecases":
        return registry["schema"]["useCases"]
    elif field == "frameworks":
        plugins = get_all_plugins(registry)
        frameworks = set()
        for p in plugins:
            frameworks.update(p.get("frameworks", []))
        return sorted(frameworks)
    return []

def main():
    parser = argparse.ArgumentParser(description="Search plugin registry")
    parser.add_argument("--tier", "-t", help="Filter by quality tier (tier-1, tier-2, etc.)")
    parser.add_argument("--category", "-c", help="Filter by category")
    parser.add_argument("--provider", "-p", help="Filter by provider tier (anthropic, vendor, community)")
    parser.add_argument("--type", "-T", help="Filter by component type (mcp, lsp, commands, etc.)")
    parser.add_argument("--usecase", "-u", help="Filter by use case")
    parser.add_argument("--framework", "-f", help="Filter by framework")
    parser.add_argument("--search", "-s", help="Search name/description")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--list", "-l", choices=["categories", "types", "providers", "tiers", "usecases", "frameworks"],
                        help="List available values for a field")
    parser.add_argument("--count", action="store_true", help="Show count only")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--marketplaces", "-m", action="store_true", help="List plugin marketplaces/sources")

    args = parser.parse_args()

    # Handle marketplaces mode
    if args.marketplaces:
        mp_data = load_marketplaces()
        marketplaces = mp_data.get("marketplaces", [])
        if args.search:
            term = args.search.lower()
            marketplaces = [m for m in marketplaces if
                           term in m.get("name", "").lower() or
                           term in m.get("description", "").lower()]
        if args.count:
            print(len(marketplaces))
        elif args.json:
            print(json.dumps(marketplaces, indent=2))
        else:
            print(format_marketplaces(marketplaces, verbose=args.verbose))
        return

    registry = load_registry()

    if args.list:
        values = list_values(registry, args.list)
        print("\n".join(values))
        return

    plugins = get_all_plugins(registry)
    filtered = filter_plugins(
        plugins,
        tier=args.tier,
        category=args.category,
        provider=args.provider,
        type=args.type,
        usecase=args.usecase,
        framework=args.framework,
        search=args.search
    )

    if args.count:
        print(len(filtered))
    elif args.json:
        print(json.dumps(filtered, indent=2))
    else:
        print(format_output(filtered, verbose=args.verbose))

if __name__ == "__main__":
    main()
