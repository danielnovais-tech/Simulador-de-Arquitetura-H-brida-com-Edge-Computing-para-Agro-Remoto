# Simulador de Arquitetura Híbrida com Edge Computing para Agro Remoto

Simula rede híbrida, edge computing resiliente e testes de validação para agricultura remota.

## 📋 Descrição

Este simulador implementa uma arquitetura híbrida de Edge Computing para monitoramento agrícola remoto, incluindo:

- **Sensores IoT**: Temperatura, umidade, pH do solo, luminosidade
- **Nós Edge**: Processamento local com cache resiliente
- **Cloud Server**: Análise centralizada e geração de alertas
- **Simulação de Falhas**: Erros de sensores e quedas de rede

## 🚀 Como Usar

### Requisitos

- Python 3.10 a 3.12
- Sem dependências externas
- Linux / macOS / Windows (WSL2 funciona bem)

### Execução

```bash
python3 simulador.py
```

### Configuração Rápida

Para teste rápido (1-2 minutos), o simulador já está configurado com `duration=120` segundos.

Para alterar a duração, edite o arquivo `simulador.py` na função `main()`:

```python
# Teste de 1 minuto
sim = Simulador(duration=60)

# Teste de 2 minutos (padrão)
sim = Simulador(duration=120)

# Teste de 5 minutos
sim = Simulador(duration=300)
```

## 📊 Saída

### Prints Durante Execução

- ✅ Prints dentro do loop principal estão **comentados** (conforme requisito)
- ✅ Prints a cada 5 ciclos são **exibidos** mostrando status dos nós
- ✅ Dashboard e relatório final são **sempre exibidos**

Exemplo de output durante execução:
```
[Ciclo 5] Status: 3/3 nós online | Dados na nuvem: 55 | Alertas: 9
[Ciclo 10] Status: 3/3 nós online | Dados na nuvem: 100 | Alertas: 22
```

### Dashboard Final

Exibe estatísticas completas:
- ⏱️ Tempo de execução
- 📡 Métricas de Edge Computing
- 🌐 Métricas de Cloud Server
- 📊 Estatísticas de sensores
- 📈 KPIs (taxa de sucesso, taxa de envio, resiliência)

### Relatório Detalhado

Mostra informações por nó Edge:
- Status (online/offline)
- Dados processados
- Falhas de rede
- Estado do cache local
- Desempenho de cada sensor

## 🔧 Personalização

Ajuste a infraestrutura em `main()`:

```python
# Configurar número de nós e sensores
sim.configurar_infraestrutura(
    num_nodes=3,        # Número de nós Edge
    sensores_por_node=4 # Sensores por nó
)
```

## 🚀 Próximos Passos

- [ ] Mini Flask + Plotly com gráficos dos KPIs em tempo real
- [ ] API REST para consulta de dados
- [ ] Visualização geográfica dos nós
- [ ] Machine Learning para previsão de falhas

## 📝 Notas

- A simulação é resiliente a falhas de rede (10% de chance por ciclo)
- Sensores têm 5% de chance de erro por leitura
- Cache local nos nós Edge mantém até 100 itens
- Alertas são gerados automaticamente para valores críticos
