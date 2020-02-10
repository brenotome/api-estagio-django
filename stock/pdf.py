import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4

class PdfRender:
    def renderRecipe(self,order):
        buffer = io.BytesIO()
        pdf = canvas.Canvas(buffer,pagesize=letter)


        pdf.setFont("Helvetica-Bold", 22)
        pdf.drawString(100, 700, "Recibo de pagamento")
        pdf.setFont("Helvetica", 18)
        pdf.drawString(100, 600, "Produto: "+order.product.name)
        pdf.drawString(100, 550, "Comprador: "+order.user.first_name+" "+order.user.last_name)
        pdf.drawString(100, 500, "Endereço : "+order.user.address)
        pdf.drawString(100, 450, "Quantidade: "+order.quantity.__str__())
        pdf.drawString(100, 400, "Preço Total: "+order.total_price.__str__())

        pdf.showPage()
        pdf.save()

        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='recipe.pdf')