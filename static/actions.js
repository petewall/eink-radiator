const imageSources = document.getElementById("image_sources")
imageSources.onchange = async (e) => {
    await fetch(`/select_source/${e.target.selectedIndex}`, {
        method: 'POST'
    })
    await getConfiguration()
}

const configurationContainer = document.getElementById('configuration')
const saveConfigButton = document.getElementById('saveConfig')

function removeConfiguration() {
    saveConfigButton.setAttribute('disabled', 'disabled')
    while (configurationContainer.firstChild) {
        configurationContainer.removeChild(configurationContainer.lastChild);
    }
}

async function getConfiguration() {
    removeConfiguration()

    let response = await fetch('/source')
    let configuration = await response.json()
    for (let key in configuration) {
        let label = document.createElement('label')
        label.setAttribute('for', key)
        label.innerText = `${key}: `
        configurationContainer.appendChild(label)

        let field = document.createElement('input')
        field.setAttribute('name', key)
        field.value = configuration[key]
        configurationContainer.appendChild(field)
    }
    saveConfigButton.removeAttribute('disabled')
}
getConfiguration()

saveConfigButton.onclick = async () => {
    let config = {}
    for (let node of configurationContainer.childNodes) {
        if (node.tagName === 'INPUT') {
            config[node.getAttribute('name')] = node.value
        }
    }

    console.log(`Saving configuration for source: ${JSON.stringify(config)}`)
    await fetch('/source', {
        method: 'PATCH',
        body: JSON.stringify(config),
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        }
    })
}