import scrapy

class MercadoLibreSpider(scrapy.Spider):
    name = "mercado_libre"
    allowed_domains = ["mercadolibre.com.co"]
    start_urls = ["https://www.mercadolibre.com.co/"]

    def parse(self, response):
        # Iterar sobre los productos de la página de inicio
        for product in response.css('li.ui-search-layout__item.shops__layout-item'):
            yield {
                'title': product.css('h2.poly-box.poly-component__title::text').get(),  # Título del producto
                'price': product.css('span.andes-money-amount.andes-money-amount--cents-superscript::text').get(),  # Precio
                'link': product.css('a.ui-search-link::attr(href)').get()  # Link del producto
            }

        # Obtener el enlace de la siguiente página si existe
        next_page = response.css('a.ui-paginator-link[title="Siguiente"]::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
