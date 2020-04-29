/* global previewImage, radiatorImage, refreshPreviewImage, refreshRadiatorImage, setImageButton  */

const imageSources = document.getElementById('image_sources')
async function loadImageSourceConfiguration() {
    previewImage.classList.add('loading')
    await fetch(`/select_source/${imageSources.selectedIndex}`, {
        method: 'POST'
    })
    await getConfiguration()
    await refreshPreviewImage()

}
imageSources.onchange = loadImageSourceConfiguration

const configurationContainer = document.getElementById('configuration')
const saveConfigButton = document.getElementById('saveConfig')

function removeConfiguration() {
    saveConfigButton.setAttribute('disabled', 'disabled')
    while (configurationContainer.firstChild) {
        configurationContainer.removeChild(configurationContainer.lastChild);
    }
}

function makeTextField(name, value, isPassword) {
    let field = document.createElement('input')
    field.setAttribute('name', name)
    if (isPassword) {
        field.setAttribute('type', 'password')
    }
    field.value = value
    return field
}

function makeSelection(name, value, options) {
    let dropdown = document.createElement('select')
    dropdown.setAttribute('name', name)
    for (let option of options) {
        let option_obj = document.createElement('option')
        option_obj.setAttribute('value', option)
        option_obj.innerText = option
        dropdown.appendChild(option_obj)
    }
    dropdown.value = value
    return dropdown
}

function makeTextArea(name, value) {
    let field = document.createElement('textarea')
    field.setAttribute('name', name)
    field.value = value
    return field
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

        if (configuration[key] == null || typeof configuration[key] === 'string') {
            configurationContainer.appendChild(makeTextField(key, configuration[key], key === 'password'))
        } else if (configuration[key].type === 'select') {
            configurationContainer.appendChild(makeSelection(key, configuration[key].value, configuration[key].options))
        } else if (configuration[key].type === 'textarea') {
            configurationContainer.appendChild(makeTextArea(key, configuration[key].value))
        }
    }
    saveConfigButton.removeAttribute('disabled')
}

saveConfigButton.onclick = async () => {
    let config = {}
    let sourceName = ""
    for (let node of configurationContainer.childNodes) {
        if (node.tagName === 'INPUT' ||
            node.tagName === 'SELECT' ||
            node.tagName === 'TEXTAREA') {
            let name = node.getAttribute('name')
            config[name] = node.value
            if (name === 'name') {
                sourceName = node.value
            }
        }
    }

    imageSources.options[imageSources.selectedIndex].innerText = sourceName
    previewImage.classList.add('loading')
    await fetch('/source', {
        method: 'PATCH',
        body: JSON.stringify(config),
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        }
    })
    await refreshPreviewImage()
}

setImageButton.onclick = async () => {
    setImageButton.setAttribute('disabled', 'disabled')
    radiatorImage.classList.add('loading')

    await fetch('/set_image', {
        method: 'POST'
    })

    await refreshRadiatorImage()
    setImageButton.removeAttribute('disabled')
}

const newSourceList = document.getElementById('new_source_list')
const addSourceButton = document.getElementById('add_source')
const deleteSourceButton = document.getElementById('delete_source')

addSourceButton.onclick = async () => {
    const name = `New ${newSourceList.value}`
    await fetch('/source', {
        method: 'POST',
        body: JSON.stringify({
            index: newSourceList.selectedIndex - 1,
            config: {name}
        }),
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        }
    })
    const newSource = document.createElement('option')
    newSource.textContent = name

    imageSources.appendChild(newSource)

    newSourceList.selectedIndex = 0
    addSourceButton.setAttribute('disabled', 'disabled')
}

deleteSourceButton.onclick = async () => {
    const index = imageSources.selectedIndex
    imageSources.remove(index)
    if (index === imageSources.length) {
        imageSources.selectedIndex = imageSources.length - 1
        await loadImageSourceConfiguration()
    }

    await fetch('/source', {
        method: 'DELETE'
    })
}

newSourceList.onchange = () => {
    if (newSourceList.selectedIndex === 0) {
        addSourceButton.setAttribute('disabled', 'disabled')
    } else {
        addSourceButton.removeAttribute('disabled')
    }
}
