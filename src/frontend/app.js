const API = 'https://localhost:7024/api/crm';
const AUTH = 'https://localhost:7024/api/auth';
const modal = new bootstrap.Modal(document.getElementById('crmModal'));
let entries = [];

// Auth guard
const user = localStorage.getItem('user');
if (!user) window.location.href = 'login.html';
document.getElementById('navUser').textContent = user;

function logout() {
  localStorage.removeItem('user');
  window.location.href = 'login.html';
}

async function load() {
  const tbody = document.getElementById('tableBody');
  try {
    const res  = await fetch(API);
    entries    = await res.json();

    if (entries.length === 0) {
      tbody.innerHTML = '<tr><td colspan="6" class="text-center py-4 text-muted">Sin registros aún</td></tr>';
      return;
    }

    tbody.innerHTML = entries.map((e, i) => `
      <tr>
        <td>${e.id}</td>
        <td>${e.customerName}</td>
        <td>${e.phone}</td>
        <td>${e.message}</td>
        <td>${new Date(e.createdAt).toLocaleDateString('es-AR')}</td>
        <td>
          <button class="btn btn-sm btn-outline-secondary me-1" onclick="edit(${e.id})">Editar</button>
          <button class="btn btn-sm btn-outline-danger"    id="btn-del-${i+1}"      onclick="remove(${e.id})">Eliminar</button>
        </td>
      </tr>`).join('');

  } catch {
    tbody.innerHTML = '<tr><td colspan="6" class="text-center py-4 text-danger">No se pudo conectar con la API</td></tr>';
  }
}

function edit(id) {
  const e = entries.find(x => x.id === id);
  document.getElementById('modalTitle').textContent  = 'Editar registro';
  document.getElementById('entryId').value           = e.id;
  document.getElementById('customerName').value      = e.customerName;
  document.getElementById('phone').value             = e.phone;
  document.getElementById('message').value           = e.message;
  modal.show();
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
