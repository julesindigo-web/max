# System Diagram Templates

## Purpose
Provide deterministic Mermaid.js templates for architecture visualization.

## General Rules
- Match node names to source inventory symbols exactly.
- Keep one abstraction level per diagram.
- Add a text summary below every diagram.
- Keep diagrams under 30 nodes. Split larger scopes.

## Context Diagram Template
- Show external actors on the left, this system center, external systems right.
- Label each edge with protocol and purpose.
- Include the following snippet pattern:
- graph LR
- actorUser[User] --> system[This System]
- system --> extPay[Payment Provider]

## Container Diagram Template
- Show gateway, services, queues, and datastores as separate nodes.
- Label edges with sync, async, or batch markers.
- Group by runtime boundary with subgraphs.

## Component Diagram Template
- Show handlers, domain modules, and adapters inside one service boundary.
- Draw dependencies from handlers toward domain and outward to adapters.
- Annotate storage access with operation type.

## Data-Flow Diagram Template
- Trace one request or event chain from entry to storage and back.
- Number steps sequentially on edges.
- Mark trust boundaries and validation points.

## Accessibility
- Provide high-contrast theme settings for rendering.
- Include a table equivalent listing nodes and edges.
- Keep edge labels short and action-oriented.
