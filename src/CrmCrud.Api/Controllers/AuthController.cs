using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using CrmCrud.Api.Data;

namespace CrmCrud.Api.Controllers;

[ApiController]
[Route("api/auth")]
public class AuthController : ControllerBase
{
    private readonly AppDbContext _db;

    public AuthController(AppDbContext db) => _db = db;

    public record LoginRequest(string Username, string Password);

    [HttpPost("login")]
    public async Task<IActionResult> Login(LoginRequest req)
    {
        var user = await _db.Users
            .FirstOrDefaultAsync(u => u.Username == req.Username && u.Password == req.Password);

        if (user is null)
            return Unauthorized(new { message = "Usuario o contraseña incorrectos." });

        return Ok(new { message = "Login exitoso.", username = user.Username });
    }
}
