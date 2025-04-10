<?php
namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Location extends Model
{
    use HasFactory;
    
    protected $connection = 'pgsql'; // Explicitly set connection
    protected $table = 'locations'; // Just table name without schema
    
    protected $fillable = [
        'location', 
        'direction'
    ];

    public $timestamps = false;
    protected $primaryKey = 'location_id';
    public $incrementing = true;
    protected $keyType = 'integer';
}