using CrmCrud.Api.Models;

namespace CrmCrud.Api.Services;

public interface ICrmService
{
    Task<IEnumerable<CrmEntry>> GetAllAsync();
    Task<CrmEntry?> GetByIdAsync(int id);
    Task<CrmEntry> CreateAsync(CrmEntry entry);
    Task<bool> UpdateAsync(int id, CrmEntry entry);
    Task<bool> DeleteAsync(int id);
}
