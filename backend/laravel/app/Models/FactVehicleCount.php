<?php
namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class FactVehicleCount extends Model
{
    protected $connection = 'dw_pgsql'; // Conexão com o Data Warehouse
    protected $table = 'warehouse_vehicle_count_db.fact_vehicle_counts';

    public function date()
    {
        return $this->belongsTo(DimDate::class, 'date_id', 'date_id'); // FK: date_id
    }

    public function location()
    {
        return $this->belongsTo(DimLocation::class, 'location_id', 'location_id'); // FK: location_id
    }

    public function time()
    {
        return $this->belongsTo(DimTime::class, 'time_id', 'time_id'); // FK: time_id
    }
}