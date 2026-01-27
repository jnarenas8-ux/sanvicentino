#!/usr/bin/env python3
"""
Script para ver el contenido de la base de datos
"""

import sys
sys.path.insert(0, '/workspaces/sanvicentino/app')

from run import app, db
from models import User, Product, Cart, CartItem, Order, OrderItem

with app.app_context():
    print("\n" + "="*80)
    print("📊 CONTENIDO DE LA BASE DE DATOS - SAN VICENTINO")
    print("="*80)
    
    # ===== USUARIOS =====
    print("\n👥 USUARIOS:")
    print("-" * 80)
    usuarios = User.query.all()
    if usuarios:
        for user in usuarios:
            role = "🔑 ADMIN" if user.is_admin else "👤 CLIENTE"
            print(f"  {role} | {user.email} | Usuario: {user.username}")
    else:
        print("  ❌ No hay usuarios registrados")
    
    # ===== PRODUCTOS =====
    print("\n📦 PRODUCTOS:")
    print("-" * 80)
    productos = Product.query.all()
    if productos:
        for prod in productos:
            status = "✅ Publicado" if prod.publicado else "⚠️ No Publicado"
            stock = f"Stock: {prod.stock}" if prod.stock > 0 else "AGOTADO"
            print(f"  [{prod.id}] {prod.nombre}")
            print(f"      Precio: S/. {prod.precio:.2f} | {stock} | {status}")
            print(f"      Categoría: {prod.categoria}")
    else:
        print("  ❌ No hay productos registrados")
    
    # ===== CARRITOS =====
    print("\n🛒 CARRITOS:")
    print("-" * 80)
    carritos = Cart.query.all()
    if carritos:
        for carrito in carritos:
            usuario = User.query.get(carrito.user_id)
            total = carrito.get_total()
            items = carrito.get_item_count()
            print(f"  Carrito ID: {carrito.id} | Usuario: {usuario.email if usuario else 'N/A'}")
            print(f"    Items: {items} | Total: S/. {total:.2f}")
    else:
        print("  ❌ No hay carritos registrados")
    
    # ===== ÓRDENES =====
    print("\n📋 ÓRDENES:")
    print("-" * 80)
    ordenes = Order.query.all()
    if ordenes:
        for orden in ordenes:
            usuario = User.query.get(orden.user_id)
            print(f"  [{orden.id}] {orden.order_number}")
            print(f"      Usuario: {usuario.email if usuario else 'N/A'}")
            print(f"      Total: S/. {orden.total:.2f} | Estado: {orden.status}")
            print(f"      Método: {orden.payment_method} | Pago: {orden.payment_status}")
    else:
        print("  ❌ No hay órdenes registradas")
    
    # ===== RESUMEN =====
    print("\n" + "="*80)
    print("📈 RESUMEN:")
    print("-" * 80)
    print(f"  Total de Usuarios: {User.query.count()}")
    print(f"  Total de Productos: {Product.query.count()}")
    print(f"  Total de Carritos: {Cart.query.count()}")
    print(f"  Total de Órdenes: {Order.query.count()}")
    print("="*80 + "\n")

