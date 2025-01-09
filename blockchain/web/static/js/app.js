const { createApp, ref, onMounted } = Vue

const app = createApp({
    setup() {
        const blocks = ref([])
        const transactions = ref([])
        const peers = ref([])
        const stats = ref({
            totalBlocks: 0,
            totalTransactions: 0,
            activeValidators: 0,
            currentDifficulty: 0
        })

        const ws = new WebSocket(`ws://${window.location.host}/ws`)

        ws.onmessage = (event) => {
            const data = JSON.parse(event.data)
            handleWebSocketMessage(data)
        }

        const handleWebSocketMessage = (data) => {
            switch (data.type) {
                case 'new_block':
                    blocks.value.unshift(data.block)
                    updateStats()
                    break
                case 'new_transaction':
                    transactions.value.unshift(data.transaction)
                    updateStats()
                    break
                case 'peer_update':
                    peers.value = data.peers
                    break
            }
        }

        const updateStats = () => {
            stats.value = {
                totalBlocks: blocks.value.length,
                totalTransactions: transactions.value.length,
                activeValidators: peers.value.filter(p => p.isValidator).length,
                currentDifficulty: blocks.value[0]?.difficulty || 0
            }
        }

        onMounted(async () => {
            const [blocksRes, txRes, peersRes] = await Promise.all([
                fetch('/api/blocks'),
                fetch('/api/transactions'),
                fetch('/api/peers')
            ])

            blocks.value = await blocksRes.json()
            transactions.value = await txRes.json()
            peers.value = await peersRes.json()
            updateStats()
        })

        return {
            blocks,
            transactions,
            peers,
            stats
        }
    }
})

app.mount('#app')
