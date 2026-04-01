const API = 'https://localhost:7024/api/crm';
const modal = new bootstrap.Modal(document.getElementById('crmModal'));

async function load() {
  const tbody = document.getElementById('tableBody');
  try {
    const res  = await fetch(API);
    const data = await res.json();
    // console.log(data);
    if (data.length === 0) {
      tbody.innerHTML = '<tr><td colspan="6" class="text-center py-4 text-muted">Sin registros aún</td></tr>';
      return;
    }

    tbody.innerHTML = data.map(e => `
      <tr>
        <td>${e.id}</td>
        <td>${e.customerName}</td>
        <td>${e.phone}</td>
        <td>${e.message}</td>
        <td>${new Date(e.createdAt).toLocaleDateString('es-AR')}</td>
        <td>
          <button class="btn btn-sm btn-outline-secondary me-1" onclick="edit(${e.id})">Editar</button>
          <button class="btn btn-sm btn-outline-danger"          onclick="remove(${e.id})">Eliminar</button>
        </td>
      </tr>`).join('');

  } catch {
    tbody.innerHTML = '<tr><td colspan="6" class="text-center py-4 text-danger">No se pudo conectar con la API</td></tr>';
  }
}

async function remove(id) {
  if (!confirm('¿Eliminar este registro?')) return;
  const res = await fetch(`${API}/${id}`, { method: 'DELETE' });
  if (res.ok || res.status === 204) {
    showAlert('Registro eliminado.', 'success');
    load();
  } else {
    showAlert('Error al eliminar.', 'danger');
  }
}

function openModal() {
  document.getElementById('modalTitle').textContent = 'Nuevo registro';
  document.getElementById('entryId').value      = '';
  document.getElementById('customerName').value = '';
  document.getElementById('phone').value        = '';
  document.getElementById('message').value      = '';
  modal.show();
}

function showAlert(msg, type) {
  const el = document.getElementById('alert');
  el.className   = `alert alert-${type}`;
  el.textContent = msg;
  setTimeout(() => (el.className = 'alert d-none'), 3000);
}
async function save() {
  const id   = document.getElementById('entryId').value;
  const body = {
    customerName: document.getElementById('customerName').value.trim(),
    phone:        document.getElementById('phone').value.trim(),
    message:      document.getElementById('message').value.trim(),
  };

  if (!body.customerName || !body.phone || !body.message)
    return showAlert('Completa todos los campos.', 'warning');

  const res = id
    ? await fetch(`${API}/${id}`, {
        method:  'PUT',
        headers: { 'Content-Type': 'application/json' },
        body:    JSON.stringify({ id: Number(id), ...body }),
      })
    : await fetch(API, {
        method:  'POST',
        headers: { 'Content-Type': 'application/json' },
        body:    JSON.stringify(body),
      });

  if (res.ok || res.status === 201 || res.status === 204) {
    modal.hide();
    showAlert(id ? 'Actualizado.' : 'Creado.', 'success');
    load();
  } else {
    showAlert('Error al guardar.', 'danger');
  }
}

load();