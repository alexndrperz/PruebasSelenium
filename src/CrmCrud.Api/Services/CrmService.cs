using Microsoft.EntityFrameworkCore;
using CrmCrud.Api.Data;
using CrmCrud.Api.Models;

namespace CrmCrud.Api.Services;

public class CrmService : ICrmService
{
    private readonly AppDbContext _db;

    public CrmService(AppDbContext db) => _db = db;

    public async Task<IEnumerable<CrmEntry>> GetAllAsync() =>
        await _db.CrmEntries.OrderByDescending(e => e.CreatedAt).ToListAsync();

    public async Task<CrmEntry?> GetByIdAsync(int id) =>
        await _db.CrmEntries.FindAsync(id);

    public async Task<CrmEntry> CreateAsync(CrmEntry entry)
    {
        entry.CreatedAt = DateTime.UtcNow;
        _db.CrmEntries.Add(entry);
        await _db.SaveChangesAsync();
        return entry;
    }

    public async Task<bool> UpdateAsync(int id, CrmEntry entry)
    {
        var existing = await _db.CrmEntries.FindAsync(id);
        if (existing is null) return false;

        existing.CustomerName = entry.CustomerName;
        existing.Phone = entry.Phone;
        existing.Message = entry.Message;

        await _db.SaveChangesAsync();
        return true;
    }

    public async Task<bool> DeleteAsync(int id)
    {
        var existing = await _db.CrmEntries.FindAsync(id);
        if (existing is null) return false;

        _db.CrmEntries.Remove(existing);
        await _db.SaveChangesAsync();
        return true;
    }
}
