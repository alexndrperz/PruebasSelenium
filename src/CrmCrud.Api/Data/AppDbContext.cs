using Microsoft.EntityFrameworkCore;
using CrmCrud.Api.Models;

namespace CrmCrud.Api.Data;

public class AppDbContext : DbContext
{
    public AppDbContext(DbContextOptions<AppDbContext> options) : base(options) { }

    public DbSet<CrmEntry> CrmEntries => Set<CrmEntry>();
}
