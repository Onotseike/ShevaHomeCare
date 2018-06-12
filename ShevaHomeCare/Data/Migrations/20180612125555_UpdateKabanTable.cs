using Microsoft.EntityFrameworkCore.Migrations;

namespace ShevaHomeCare.Data.Migrations
{
    public partial class UpdateKabanTable : Migration
    {
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.AddColumn<string>(
                name: "Status",
                table: "KabanItemsData",
                nullable: true);
        }

        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(
                name: "Status",
                table: "KabanItemsData");
        }
    }
}
