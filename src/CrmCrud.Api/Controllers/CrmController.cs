using Microsoft.AspNetCore.Mvc;
using CrmCrud.Api.Models;
using CrmCrud.Api.Services;

namespace CrmCrud.Api.Controllers;

[ApiController]
[Route("api/[controller]")]
public class CrmController : ControllerBase
{
    private readonly ICrmService _service;

    public CrmController(ICrmService service) => _service = service;

    [HttpGet]
    public async Task<IActionResult> GetAll() =>
        Ok(await _service.GetAllAsync());

    [HttpGet("{id}")]
    public async Task<IActionResult> GetById(int id)
    {
        var entry = await _service.GetByIdAsync(id);
        return entry is null ? NotFound() : Ok(entry);
    }

    [HttpPost]
    public async Task<IActionResult> Create(CrmEntry entry)
    {
        var created = await _service.CreateAsync(entry);
        return CreatedAtAction(nameof(GetById), new { id = created.Id }, created);
    }

    [HttpPut("{id}")]
    public async Task<IActionResult> Update(int id, CrmEntry entry)
    {
        if (id != entry.Id) return BadRequest();
        return await _service.UpdateAsync(id, entry) ? NoContent() : NotFound();
    }

    [HttpDelete("{id}")]
    public async Task<IActionResult> Delete(int id) =>
        await _service.DeleteAsync(id) ? NoContent() : NotFound();
}
