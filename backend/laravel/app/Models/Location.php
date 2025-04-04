<?php
namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Location extends Model
{
    use HasFactory;

    protected $table = 'location';

    protected $fillable = [
        'location', 
        'direction',
    ];

    public $timestamps = false;

    protected $primaryKey = 'location_id'; // Especifica a chave primária
    public $incrementing = false; // Define se a chave primária é auto-incrementada
    protected $keyType = 'string'; // Define o tipo da chave primária (se necessário)
}
