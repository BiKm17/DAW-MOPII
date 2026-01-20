
package com.tienda.forestal.repository;

import com.tienda.forestal.model.Producto;
import org.springframework.data.jpa.repository.JpaRepository;

/**
 * Repository de Producto
 * Spring genera automáticamente las consultas SQL
 */
public interface ProductoRepository extends JpaRepository<Producto, Integer> {
}

