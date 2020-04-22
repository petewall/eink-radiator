function bufferToBase64(buffer) {
    let binary = '';
    let bytes = [].slice.call(new Uint8Array(buffer))
    bytes.forEach((b) => binary += String.fromCharCode(b))
    return window.btoa(binary)
}

async function refreshImage(url, image) {
    let response = await fetch(url)
    if (response.status === 200) {
        let buffer = await response.arrayBuffer()
        image.style.backgroundImage = `url("data:image/png;base64,${bufferToBase64(buffer)}")`
    } else {
        image.style.backgroundImage = ""
    }
    image.classList.remove('loading')
}

const previewImage = document.getElementById('preview-image')
const radiatorImage = document.getElementById('radiator-image')

let refreshPreviewImage = () => refreshImage('/preview-image.png', previewImage)
let refreshRadiatorImage = () => refreshImage('/radiator-image.png', radiatorImage)

const imageSources = document.getElementById("image_sources")
imageSources.onchange = async (e) => {
    previewImage.classList.add('loading')
    await fetch(`/select_source/${e.target.selectedIndex}`, {
        method: 'POST'
    })
    await getConfiguration()
    await refreshPreviewImage()
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

        if (typeof configuration[key] === 'string') {
            let field = document.createElement('input')
            field.setAttribute('name', key)
            if (key === 'password') {
                field.setAttribute('type', 'password')
            }
            field.value = configuration[key]
            configurationContainer.appendChild(field)
        } else {
            let dropdown = document.createElement('select')
            dropdown.setAttribute('name', key)
            for (let option of configuration[key].options) {
                let option_obj = document.createElement('option')
                option_obj.setAttribute('value', option)
                option_obj.innerText = option
                dropdown.appendChild(option_obj)
            }
            dropdown.value = configuration[key].value
            configurationContainer.appendChild(dropdown)
        }
    }
    saveConfigButton.removeAttribute('disabled')
}

saveConfigButton.onclick = async () => {
    let config = {}
    for (let node of configurationContainer.childNodes) {
        if (node.tagName === 'INPUT' || node.tagName === 'SELECT') {
            config[node.getAttribute('name')] = node.value
        }
    }

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

const setImageButton = document.getElementById('setImage')
setImageButton.onclick = async () => {
    setImageButton.setAttribute('disabled', 'disabled')
    radiatorImage.classList.add('loading')

    await fetch('/set_image', {
        method: 'POST'
    })

    await refreshRadiatorImage()
    setImageButton.removeAttribute('disabled')
}

refreshPreviewImage()
refreshRadiatorImage()
getConfiguration()
