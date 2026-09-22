import streamlit as st
import ipaddress
import math

st.title("Calculadora Genérica VLSM")

red_input = st.text_input("Red base (ej. 192.150.0.0/16)", "192.150.0.0/16")

st.write("Introduce el número de hosts para cada subred (de mayor a menor):")
hosts_clientes = st.number_input("Clientes", min_value=1, value=230)
hosts_dist = st.number_input("Distribuidores", min_value=1, value=120)
hosts_com = st.number_input("Comerciales", min_value=1, value=10)
hosts_enlace1 = st.number_input("Enlace 1", min_value=1, value=6)
hosts_enlace2 = st.number_input("Enlace 2", min_value=1, value=6)
hosts_enlace3 = st.number_input("Enlace 3", min_value=1, value=6)

if st.button("Calcular Esquema VLSM"):
    try:
        red_base = ipaddress.IPv4Network(red_input)
        requisitos = [
            ("Clientes", hosts_clientes),
            ("Distribuidores", hosts_dist),
            ("Comerciales", hosts_com),
            ("Enlace 1", hosts_enlace1),
            ("Enlace 2", hosts_enlace2),
            ("Enlace 3", hosts_enlace3)
        ]
        
        # Reordenar automáticamente de mayor a menor por si el usuario se equivoca
        requisitos.sort(key=lambda x: x[1], reverse=True)
        
        ip_actual = red_base.network_address
        
        for nombre, hosts in requisitos:
            bits_host = math.ceil(math.log2(hosts + 2))
            prefijo = 32 - bits_host
            subred_calc = ipaddress.IPv4Network(f"{ip_actual}/{prefijo}")
            
            st.subheader(f"Red: {nombre} ({hosts} hosts)")
            st.write(f"**Dirección:** {subred_calc.network_address}/{prefijo}")
            st.write(f"**Máscara:** {subred_calc.netmask}")
            st.write(f"**Rango útil:** {subred_calc[1]} - {subred_calc[-2]}")
            st.write(f"**Broadcast:** {subred_calc.broadcast_address}")
            
            ip_actual = subred_calc.broadcast_address + 1
            
    except ValueError:
        st.error("Por favor, introduce una red base válida con su notación CIDR.")
