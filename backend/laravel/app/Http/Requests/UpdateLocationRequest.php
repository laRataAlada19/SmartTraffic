<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class UpdateLocationRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true;
    }
    
    public function rules(): array
    {
        return [
            'location' => 'nullable|string|max:100',
            'direction' => 'nullable|string|max:50',
            'latitude' => 'nullable|string|max:50',
            'longitude' => 'nullable|string|max:50',
        ];
    }
}
