const form = document.querySelector('#form');


let automoviles = [];
let editar = false;
let automovilId = null;


window.addEventListener('DOMContentLoaded', async () => {
    const response = await fetch("/jonathan/automovil")
    const data = await response.json()
    automoviles = data
    console.log(data)
    renderAutomovil(automoviles)
})


form.addEventListener('submit', async e => {
    e.preventDefault()

    const marca = form['marca'].value;
    const modelo = form['modelo'].value;
    const fecha = form['fecha'].value;
    const duenos = form['duenos'].value;
    const costos = form['costos'].value;
    const choques = form['choques'].value;

    console.log(marca, modelo, fecha, duenos, costos, choques)

    if (!editar) {
        const response = await fetch('/jonathan/automovil', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                marca,
                modelo,
                fecha,
                duenos,
                costos,
                choques
            })
        })

        const data = await response.json();
        console.log(data);
        automoviles.unshift(data);
        renderAutomovil(automoviles)
        form.reset()
    }
    else {
        const response = await fetch(`/jonathan/automovil/${automovilId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                marca,
                modelo,
                fecha,
                duenos,
                costos,
                choques
            })
        })

        const updataAutomovil = await response.json()
        automoviles = automoviles.map(automovil => automovil.id === updataAutomovil.id ? updataAutomovil : automovil)
        renderAutomovil(automoviles)
        editar = false
        automovilId = null
    }

    renderAutomovil(automoviles);
    form.reset();

});

function renderAutomovil(automoviles) {
    const automovilList = document.querySelector('#automovilList')
    automovilList.innerHTML = ""
    automoviles.forEach(automovil => {
        const automovilItem = document.createElement('li')
        automovilItem.classList = 'list-group list-group-item-dark my-2'
        automovilItem.innerHTML = `
        <header>
        <div>
        <h3>${automovil.marca}  ${automovil.modelo}</h3>
        </div>
        </header>
        <body    >
        <p>
        ${automovil.fecha}
        </p>
         <p>
        ${automovil.duenos}
        </p>
         <p>
        ${automovil.costos}
        </p>
         <p>
        ${automovil.choques}
        </p>
        <div class="d-flex align-items-center;">
            <button class="btn-delete btn btn-danger">borrar</button>
            <button class="btn-edit btn  btn-danger "  >actualizar</button>
        </div>
        
        </body>
        `

        const btnDelete = automovilItem.querySelector('.btn-delete')

        btnDelete.addEventListener('click', async () => {
            console.log(automovil.id)
            const response = await fetch(`/jonathan/automovil/${automovil.id}`, {
                method: 'DELETE',
            })
            const data = await response.json()
            console.log(data)
            automoviles = automoviles.filter(automovil => automovil.id !== data.id)
            renderAutomovil(automoviles)
        })

        const btnEdit = automovilItem.querySelector('.btn-edit')

        btnEdit.addEventListener('click', async () => {
            console.log(automovil.id)
            const response = await fetch(`/jonathan/automovil/${automovil.id}`)
            const data = await response.json()

            form['marca'].value = data.marca;
            form['modelo'].value = data.modelo;
            form['fecha'].value = data.fecha;
            form['duenos'].value = data.duenos;
            form['costos'].value = data.costos;
            form['choques'].value = data.choques;

            editar = true
            console.log(data)
            automovilId = automovil.id
        })





        console.log(automovilItem);
        automovilList.append(automovilItem);
    })
}