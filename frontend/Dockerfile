# Imagen base de Nginx para servir archivos estáticos
FROM nginx:alpine

# Eliminar configuración por defecto de Nginx
RUN rm -rf /usr/share/nginx/html/*

# Copiar los archivos del frontend
COPY . /usr/share/nginx/html

# Copiar configuración personalizada de Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Puerto expuesto
EXPOSE 80

# Nginx arranca automáticamente
CMD ["nginx", "-g", "daemon off;"]
